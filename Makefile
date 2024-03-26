setup: python env docker-install network kafka-cluster airflow spark-app

python:
	sudo apt-get update && sudo apt-get install -y python3-venv

env:
	python3 -m venv .venv && \
	. .venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt

docker-install:
	sudo apt-get update && \
	sudo apt-get install -y \
	    apt-transport-https \
	    ca-certificates \
	    curl \
	    gnupg \
	    lsb-release && \
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
	echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null && \
	sudo apt-get update && \
	sudo apt-get install -y docker-ce docker-ce-cli containerd.io && \
	sudo usermod -aG docker $(whoami)

network: docker-install
	docker network create airflow-kafka

kafka-cluster: docker-install
	docker-compose up -d

airflow: kafka-cluster
	docker-compose -f docker-compose-airflow.yaml up -d && \
	echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_PROJ_DIR=\"./airflow_resources\"" > .env

spark-app: docker-install
	docker build -f spark/Dockerfile -t earthquakes/spark:latest --build-arg POSTGRES_PASSWORD=admin .
