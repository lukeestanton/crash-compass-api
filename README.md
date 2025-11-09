# Crash Compass API

Crash Compass API is a FastAPI service that exposes economic data used by the Crash Compass project. It serves FRED time-series that are synchronized into a local database and grouped into thematic categories for downstream consumers (for example, a front-end "dial" UI).

## Features

- Health check endpoint for deployment monitoring.
- REST endpoints for retrieving cached FRED time-series and their metadata.
- Scripted workflow for initializing the database and populating it with selected FRED series.

## Prerequisites

- Python 3.10 or later
- A relational database that SQLAlchemy can connect to (SQLite, PostgreSQL, etc.)
- A [FRED](https://fred.stlouisfed.org/docs/api/api_key.html) API key

## Installation

1. Clone the repository and change into the project directory.
2. Create and activate a Python virtual environment.
3. Install dependencies:

   ```bash
   pip install fastapi uvicorn[standard] python-dotenv SQLAlchemy fredapi
   ```

## Configuration

Create a `.env` file (or export environment variables) with the following settings:

- `DATABASE_URL` – SQLAlchemy-compatible URL for your database connection (e.g., `sqlite:///./crash_compass.db`).
- `FRED_API_KEY` – Your FRED API key used by the ingestion scripts.
- `ALLOW_ORIGINS` – (Optional) Comma-separated list of CORS origins allowed to call the API. Defaults to `http://localhost:3000` if omitted.

## Database Setup & Data Ingestion

1. Initialize the schema:

   ```bash
   python -m scripts.init_db
   ```

2. Populate the database with FRED series defined in `app/lib/series_defs.py`:

   ```bash
   python -m scripts.fetch_and_store
   ```

   The ingestion script fetches the configured series, stores their metadata in the `series` table, and persists observations in the `observations` table.

## Running the API

Start a development server with Uvicorn:

```bash
uvicorn app.main:app --reload
```

By default the server listens on `http://127.0.0.1:8000`.

## Available Endpoints

- `GET /healthz` – Simple health check returning `{ "ok": true }`.
- `GET /api/v1/fred/series/{series_id}?start=YYYY-MM-DD&end=YYYY-MM-DD` – Retrieve observations and metadata for a stored FRED series, optionally filtered by date range.
- `GET /api/v1/fred/categories` – List available categories and the series they contain.
- `GET /api/v1/fred/dial_score` – Returns the current dial score (placeholder value for now).

Interactive API docs are available at `http://127.0.0.1:8000/docs` when the server is running.

## Project Structure

```
app/
  main.py              # FastAPI application setup
  routers/             # Route definitions (FRED endpoints)
  services/            # Domain logic for FRED data access
  db/                  # SQLAlchemy models and session configuration
  lib/                 # Supporting constants and definitions
scripts/
  init_db.py           # Create database schema
  fetch_and_store.py   # Download and store FRED series in the database
```

## Contributing

1. Create a feature branch.
2. Make your changes and ensure the API runs locally.
3. Submit a pull request with a clear description of your changes.

## License

This project is proprietary and intended for internal use. Contact the maintainers for licensing information.
