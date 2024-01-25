#!/bin/sh

echo "Apply migrations to database"
python -m alembic upgrade head

echo "Start application"
python -m src
