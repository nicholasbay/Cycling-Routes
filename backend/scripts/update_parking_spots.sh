#!/bin/bash
set -e

cd /app

echo "[$(date)] Updating parking spots data..."

python scripts/fetch_parking_spots.py >> /var/log/cron.log 2>&1
if [ $? -ne 0 ]; then
    echo "[$(date)] Error fetching parking spots data." >> /var/log/cron.log
    exit 1
fi

python scripts/load_parking_spots.py >> /var/log/cron.log 2>&1
if [ $? -ne 0 ]; then
    echo "[$(date)] Error loading parking spots into database." >> /var/log/cron.log
    exit 1
fi

echo "[$(date)] Successfully updated parking spots data."
