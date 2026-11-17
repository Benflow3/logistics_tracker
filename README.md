# Logistics Tracker

## GitHub Codespaces

Open the repository in a Codespace. The dev container starts the application
container and a PostgreSQL 16 service; the API container connects to PostgreSQL
using the `postgres` service name. Python dependencies are installed after the
container is created.

Start the API from the workspace:

```bash
uvicorn src.main:app --reload --host 0.0.0.0
```

The API is available on port 8000, and PostgreSQL is available on port 5432.
The development database credentials are `postgres` / `postgres`; do not use
these credentials outside local development.

## Tests

Tests use the separate `TEST_DATABASE_URL` from `.env`. Its database name must
contain `test` and must differ from `DATABASE_URL`. In the dev container, create
the example database once with:

```bash
docker compose -f .devcontainer/docker-compose.yml exec postgres createdb -U postgres logistics_test_db
```

Then run the tests with:

```bash
python -m pytest
```
