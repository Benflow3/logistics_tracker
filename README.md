# Logistics Tracker

## GitHub Codespaces

Open the repository in a Codespace. The dev container starts the application
container and a PostgreSQL 16 service; the API container connects to PostgreSQL
using the `postgres` service name. Python dependencies are installed after the
container is created.

Start the API from the workspace:

```bash
uvicorn main:app --app-dir src --reload --host 0.0.0.0
```

The API is available on port 8000, and PostgreSQL is available on port 5432.
The development database credentials are `postgres` / `postgres`; do not use
these credentials outside local development.
