#!/bin/sh
set -e

export PYTHONPATH=/app:$PYTHONPATH

echo "Waiting for database to start..."
sleep 5

echo "Postgres is up - running migrations"

echo "Running Alembic migrations..."
alembic -c alembic.ini upgrade head

exec "$@"
