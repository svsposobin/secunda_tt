#!/bin/bash

set -e

echo "Applying database migrations..."
alembic upgrade head

echo "Starting uvicorn server..."
exec python src/core/root/main.py
