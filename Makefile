setup: python env network kafka-cluster airflow spark-app

python:
    sudo apt-get update && sudo apt-get install -y python3-venv

env:
    python3 -m venv .venv && \
    . .venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

network:
    docker network create airflow-kafka

kafka-cluster:
    docker-compose up -d

airflow:
    docker-compose -f docker-compose-airflow.yaml up -d && \
    echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_PROJ_DIR=\"./airflow_resources\"" > .env

spark-app:
    docker build -f spark/Dockerfile -t earthquakes/spark:latest --build-arg POSTGRES_PASSWORD=admin .
