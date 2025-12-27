#!/usr/bin/env python3
"""
Script to load bicycle parking data from NDJSON file into PostgreSQL database.
Reads bicycle_parking_data.ndjson and populates the parking_spots table.
Uses batch processing (1000 records) for efficiency.
"""

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


ROOT_PATH = Path(__file__).resolve().parent.parent
LOGS_PATH = ROOT_PATH / 'logs'
LOGS_PATH.mkdir(exist_ok=True)
DATA_PATH = ROOT_PATH / 'data'
DATA_PATH.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=LOGS_PATH / 'load_parking_spots.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Constants
NDJSON_FILE = DATA_PATH / 'bicycle_parking_data.ndjson'
TABLE_NAME = 'parking_spots'
BATCH_SIZE = 1000


def get_db_connection():
    """
    Create and return a PostgreSQL database connection.
    
    Returns:
        Connection object or None on failure
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            port=os.getenv('POSTGRES_PORT', '5432'),
            database=os.getenv('POSTGRES_DATABASE'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD')
        )
        logging.info("Successfully connected to PostgreSQL database")
        return conn
    except psycopg2.Error as e:
        logging.error(f"Failed to connect to database: {e}")
        return None


def verify_table_exists(conn):
    """
    Verify that the parking_spots table exists in the database.
    
    Args:
        conn: PostgreSQL connection object
        
    Returns:
        True if table exists, False otherwise
    """
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = %s
            );
        """, (TABLE_NAME,))
        
        exists = cursor.fetchone()[0]
        cursor.close()
        
        if exists:
            logging.info(f"Table '{TABLE_NAME}' verified to exist")
        else:
            logging.error(f"Table '{TABLE_NAME}' does not exist")
        
        return exists
    except psycopg2.Error as e:
        logging.error(f"Error verifying table existence: {e}")
        return False


def read_ndjson_file():
    """
    Read and parse the NDJSON file.
    
    Yields:
        Dictionary representing each parking spot record
    """
    try:
        with open(NDJSON_FILE, 'r') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    record = json.loads(line.strip())
                    yield record
                except json.JSONDecodeError as e:
                    logging.warning(f"Skipping invalid JSON at line {line_num}: {e}")
                    continue
    except FileNotFoundError:
        logging.error(f"File not found: {NDJSON_FILE}")
        sys.exit(1)
    except IOError as e:
        logging.error(f"Error reading file {NDJSON_FILE}: {e}")
        sys.exit(1)


def prepare_batch_data(records):
    """
    Transform records into format suitable for database insertion.
    
    Args:
        records: List of dictionaries from NDJSON
        
    Returns:
        List of tuples ready for database insertion
    """
    batch_data = []
    for record in records:
        # Map NDJSON fields to database columns
        # Note: PostgreSQL POINT uses (longitude, latitude) order
        data = (
            record.get('Description'),
            record.get('Longitude'),  # longitude first for POINT
            record.get('Latitude'),   # latitude second for POINT
            record.get('RackType'),
            record.get('RackCount'),
            record.get('ShelterIndicator')
        )
        batch_data.append(data)
    return batch_data


def insert_batch(conn, batch_data):
    """
    Insert a batch of records into the database using upsert logic.
    
    Args:
        conn: PostgreSQL connection object
        batch_data: List of tuples to insert
        
    Returns:
        Number of records processed, or None on error
    """
    upsert_query = """
        INSERT INTO parking_spots (description, coordinates, rack_type, rack_count, shelter_indicator)
        VALUES (%s, ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s, %s, %s)
        ON CONFLICT (description) 
        DO UPDATE SET 
            coordinates = EXCLUDED.coordinates,
            rack_type = EXCLUDED.rack_type,
            rack_count = EXCLUDED.rack_count,
            shelter_indicator = EXCLUDED.shelter_indicator;
    """
    
    try:
        cursor = conn.cursor()
        cursor.executemany(upsert_query, batch_data)
        conn.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected
    except psycopg2.Error as e:
        logging.error(f"Database error during batch insert: {e}")
        conn.rollback()
        return None


def main():
    """Main execution function."""
    logging.info("=" * 80)
    logging.info("Starting database import process")
    start_time = datetime.now()
    
    # Load environment variables
    load_dotenv()
    
    # Verify required environment variables
    required_vars = ['POSTGRES_HOST', 'POSTGRES_DATABASE', 'POSTGRES_USER', 'POSTGRES_PASSWORD']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logging.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        print(f"Error: Missing environment variables: {', '.join(missing_vars)}")
        print("Please add them to your .env file")
        sys.exit(1)
    
    # Connect to database
    conn = get_db_connection()
    if not conn:
        print("Error: Failed to connect to database. Check logs for details.")
        sys.exit(1)
    
    # Verify table exists
    if not verify_table_exists(conn):
        print(f"Error: Table '{TABLE_NAME}' does not exist in database")
        conn.close()
        sys.exit(1)
    
    # Process records in batches
    batch = []
    total_records = 0
    successful_batches = 0
    failed_batches = 0
    batch_number = 0
    
    logging.info(f"Reading records from {NDJSON_FILE}")
    
    for record in read_ndjson_file():
        batch.append(record)
        total_records += 1
        
        # Process batch when it reaches BATCH_SIZE
        if len(batch) >= BATCH_SIZE:
            batch_number += 1
            batch_data = prepare_batch_data(batch)
            
            logging.info(f"Processing batch {batch_number} ({len(batch)} records)")
            
            rows_affected = insert_batch(conn, batch_data)
            
            if rows_affected is not None:
                successful_batches += 1
                logging.info(f"  Batch {batch_number} completed: {rows_affected} rows affected")
            else:
                failed_batches += 1
                logging.warning(f"  ✗ Batch {batch_number} failed")
            
            # Clear batch for next iteration
            batch = []
    
    # Process any remaining records in final partial batch
    if batch:
        batch_number += 1
        batch_data = prepare_batch_data(batch)
        
        logging.info(f"Processing final batch {batch_number} ({len(batch)} records)")
        
        rows_affected = insert_batch(conn, batch_data)
        
        if rows_affected is not None:
            successful_batches += 1
            logging.info(f"  Final batch completed: {rows_affected} rows affected")
        else:
            failed_batches += 1
            logging.warning(f"  ✗ Final batch failed")
    
    # Close database connection
    conn.close()
    logging.info("Database connection closed")
    
    # Summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    logging.info("-" * 80)
    logging.info(f"Import completed in {duration:.2f} seconds")
    logging.info(f"Total records processed: {total_records}")
    logging.info(f"Total batches: {batch_number}")
    logging.info(f"Successful batches: {successful_batches}")
    logging.info(f"Failed batches: {failed_batches}")
    logging.info("=" * 80)
    
    print(f"Import completed: {total_records} records processed in {batch_number} batches")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Successful batches: {successful_batches}/{batch_number}")
    if failed_batches > 0:
        print(f"Failed batches: {failed_batches}")
    print(f"Log: {LOGS_PATH / 'load_parking_spots.log'}")


if __name__ == '__main__':
    main()
