setup: python env docker-install network kafka-cluster airflow spark-app

python:
	@sudo apt-get update && sudo apt-get install -y python3-venv

env:
	@python3 -m venv .venv && \
	. .venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt

docker-install:
	@sudo apt-get update && \
	sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common && \
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - && \
	sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" && \
	sudo apt-get update && \
	sudo apt-get install -y docker-ce

network:
	@docker network create airflow-kafka

kafka-cluster:
	@docker-compose up -d

airflow:
	@docker-compose -f docker-compose-airflow.yaml up -d && \
	echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_PROJ_DIR=\"./airflow_resources\"" > .env

spark-app:
	@docker build -f spark/Dockerfile -t earthquakes/spark:latest --build-arg POSTGRES_PASSWORD=admin .
