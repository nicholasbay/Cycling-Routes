# Cycling Routes

Finds cycling routes.

## Frontend

*WIP*

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
