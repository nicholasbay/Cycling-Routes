# PitStop

## Overview

Leisure cycling in Singapore has been and still is popular, but traditional bike rental models make longer, point-to-point routes inconvenient and costly. Bikes often have to be returned to the original outlet, and night rentals are priced higher due to manned operations of the rental outlets.

Dockless bike-sharing services such as Anywheel and HelloRide offer a compelling alternative. Their multi-use passes allow unlimited rides, provided each trip stays within a fixed duration (e.g., 30 minutes). For longer routes, riders could **hypothetically** "reset the timer" by parking and unlocking the bike at designated parking spots along the way.

Navigating between the designated parking spots every 30 minutes can be a hassle while out on a leisure cycle, and PitStop aims to alleviate that burden. Simply enter the start and end points, together with the preferred time intervals, and it maps out a route with the intermediate parking spots where you can reset the timer at.

## Frontend

### Local Development

1. Install project dependencies.

    ```bash
    npm install
    # or
    yarn
    # or
    pnpm install
    ```

2. Start the local development client.

    ```bash
    npm run dev
    # or
    yarn dev
    # or
    pnpm dev
    ```

3. Visit the local development client at `http://localhost:3000`.

## Backend

### Local Development

1. Create a PostgreSQL database and activate the PostGIS extension. PostGIS is used for storing the coordinates of parking spots and accurately determining the distances between a point on the route and its nearest parking spot.

2. Create a `.env` file as per `.env.example` and update the environment variables within.

3. Create a virtual environment and activate it. Use Python 3.12.

    ```bash
    cd backend
    python -m venv ./.venv
    source ./.venv/bin/activate  # Unix
    .\.venv\Scripts\activate.bat  # Windows CMD
    .\.venv\Scripts\Activate.ps1  # Windows PowerShell
    ```

4. Install project dependencies.

    ```bash
    pip install -r ./backend/requirements.txt
    ```

5. Start the local development server.

    ```bash
    uvicorn app.main:app --reload
    ```
