#!/bin/bash

# Python setup
sudo apt-get update && sudo apt-get install -y python3-venv
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create network if not exists
if ! docker network inspect airflow-kafka >/dev/null 2>&1; then
    docker network create airflow-kafka
else
    echo "Network 'airflow-kafka' already exists."
fi

# Start Kafka cluster
docker compose up -d

# Start Airflow
docker compose -f docker-compose-airflow.yaml up -d
echo "AIRFLOW_UID=$(id -u)" > .env
echo "AIRFLOW_PROJ_DIR=\"./airflow_resources\"" >> .env

# Build Spark app Docker image
docker build -f spark/Dockerfile -t earthquakes/spark:latest --build-arg POSTGRES_PASSWORD=admin .
