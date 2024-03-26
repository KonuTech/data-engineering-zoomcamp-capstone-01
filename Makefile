setup: python env network kafka-cluster airflow spark-app

python:
	sudo apt-get update && sudo apt-get install -y python3-venv

env:
	python3 -m venv .venv && \
	. .venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt

network:
	@if ! docker network inspect airflow-kafka >/dev/null 2>&1 ; then \
		docker network create airflow-kafka ; \
	else \
		echo "Network 'airflow-kafka' already exists." ; \
	fi

kafka-cluster:
	docker compose up -d

airflow:
	@echo "AIRFLOW_UID=197609" > .env && \
    echo "AIRFLOW_PROJ_DIR=./airflow_resources" >> .env && \
	docker compose -f docker-compose-airflow.yaml up -d

spark-app:
	docker build -f spark/Dockerfile -t earthquakes/spark:latest --build-arg POSTGRES_PASSWORD=admin .
