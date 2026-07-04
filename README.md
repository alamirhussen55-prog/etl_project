# Weather ETL Project

This project implements a simple ETL pipeline that fetches current weather data from the WeatherAPI, transforms it into a tabular format, and loads it into a PostgreSQL database.

## Overview

The pipeline performs three steps:

1. Extract: retrieves weather data from the Weather API.
2. Transform: normalizes the JSON payload into a pandas DataFrame and cleans the data.
3. Load: writes the transformed data into a PostgreSQL table named `weather`.

## Project Files

- `main.py` - Contains the ETL logic and pipeline orchestration.
- `docker-compose.yml` - Starts PostgreSQL and pgAdmin containers.
- `requirements.txt` - Python dependencies required for the project.
- `udemy.csv` - Sample dataset included in the workspace.

## Prerequisites

- Python 3.9+
- Docker Desktop
- A WeatherAPI key

## Environment Variables

Create a `.env` file in the project root with the following values:

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=weatherdb
WEATHER_API_KEY=your_weather_api_key_here
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=admin
```

## Installation

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

2. Start the database services:

```bash
docker compose up -d
```

3. Run the ETL pipeline:

```bash
python main.py
```

## Database Access

- PostgreSQL is exposed on port `5432`.
- pgAdmin is available at `http://localhost:8080`.

## Notes

- The script uses the `WEATHER_API_KEY` environment variable first, with a fallback value in `main.py`.
- If the database container is not ready yet, wait a few seconds and rerun the pipeline.
