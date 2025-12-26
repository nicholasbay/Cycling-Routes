#!/usr/bin/env python3
"""
Script to fetch bicycle parking data from LTA DataMall API.
Queries BicycleParkingv2 endpoint for locations defined in locations.json.
Runs monthly via cron job to update parking spot data.
"""

import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv


ROOT_PATH = Path(__file__).resolve().parent.parent
LOGS_PATH = ROOT_PATH / 'logs'
LOGS_PATH.mkdir(exist_ok=True)
DATA_PATH = ROOT_PATH / 'data'
DATA_PATH.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=LOGS_PATH / 'fetch_bicycle_parking.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Constants
API_URL = 'https://datamall2.mytransport.sg/ltaodataservice/BicycleParkingv2'
DIST = 5  # Distance in kilometers
LOCATIONS_FILE = DATA_PATH / 'locations.json'
OUTPUT_FILE = DATA_PATH / 'bicycle_parking_data.ndjson'
REQUEST_DELAY_S = 1  # Seconds between requests


def load_locations():
    """Load location data from locations.json file."""
    try:
        with open(LOCATIONS_FILE, 'r') as f:
            locations = json.load(f)
        logging.info(f"Loaded {len(locations)} locations from {LOCATIONS_FILE}")
        return locations
    except FileNotFoundError:
        logging.error(f"File not found: {LOCATIONS_FILE}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in {LOCATIONS_FILE}: {e}")
        sys.exit(1)


def fetch_bicycle_parking(lat, lon, account_key):
    """
    Fetch bicycle parking data from LTA DataMall API.
    
    Args:
        lat: Latitude coordinate
        lon: Longitude coordinate
        account_key: API account key for authentication
        
    Returns:
        List of bicycle parking records or None on error
    """
    params = {
        'Lat': lat,
        'Long': lon,
        'Dist': DIST
    }
    
    headers = {
        'AccountKey': account_key
    }
    
    try:
        response = requests.get(API_URL, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        return data.get('value', [])
    
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed for lat={lat}, lon={lon}: {e}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON response for lat={lat}, lon={lon}: {e}")
        return None


def main():
    """Main execution function."""
    logging.info("=" * 80)
    logging.info("Starting bicycle parking data fetch")
    start_time = datetime.now()
    
    # Load environment variables
    load_dotenv()
    account_key = os.getenv('DATAMALL_ACCOUNT_KEY')
    
    if not account_key:
        logging.error("DATAMALL_ACCOUNT_KEY not found in .env file")
        sys.exit(1)
    
    # Load locations
    locations = load_locations()
    
    # Fetch data for all locations
    all_records = []
    success_count = 0
    failure_count = 0
    
    for i, location in enumerate(locations, 1):
        location_id = location['ID']
        lat = location['Latitude']
        lon = location['Longitude']
        desc = location['Description']
        
        logging.info(f"Processing location {i}/{len(locations)}: ID={location_id}, {desc}")
        
        records = fetch_bicycle_parking(lat, lon, account_key)
        
        if records is not None:
            success_count += 1
            record_count = len(records)
            all_records.extend(records)
            logging.info(f"  Retrieved {record_count} bicycle parking records")
        else:
            failure_count += 1
            logging.warning(f"  Failed to retrieve data for location {location_id}")
        
        # Delay between requests (except after the last one)
        if i < len(locations):
            time.sleep(REQUEST_DELAY_S)
    
    # Write results to NDJSON file
    try:
        with open(OUTPUT_FILE, 'w') as f:
            for record in all_records:
                f.write(json.dumps(record) + '\n')
        
        logging.info(f"Successfully wrote {len(all_records)} records to {OUTPUT_FILE}")
    except IOError as e:
        logging.error(f"Failed to write output file {OUTPUT_FILE}: {e}")
        sys.exit(1)
    
    # Summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    logging.info("-" * 80)
    logging.info(f"Fetch completed in {duration:.2f} seconds")
    logging.info(f"Locations processed: {len(locations)}")
    logging.info(f"Successful requests: {success_count}")
    logging.info(f"Failed requests: {failure_count}")
    logging.info(f"Total records retrieved: {len(all_records)}")
    logging.info("=" * 80)
    
    print(f"Fetch completed: {len(all_records)} records from {success_count}/{len(locations)} locations")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Output: {OUTPUT_FILE}")
    print(f"Log: {LOGS_PATH / 'fetch_bicycle_parking.log'}")


if __name__ == '__main__':
    main()
