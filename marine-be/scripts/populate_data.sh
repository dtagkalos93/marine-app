#! /usr/bin/env bash

docker-compose down
docker-compose build
docker-compose up -d
sleep 5
poetry run python command/populate_db.py