#! /usr/bin/env bash

docker-compose down
docker-compose build
docker-compose up -d db
sleep 2
alembic upgrade head
pytest --cov=app --cov-report=html