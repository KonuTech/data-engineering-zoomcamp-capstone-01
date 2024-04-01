from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator

from src.kafka_client.kafka_earthquakes_batch import batch

start_date = datetime.today() - timedelta(days=1)

default_args = {
    "owner": "airflow",
    "start_date": start_date,
    "retries": 2,  # number of retries before failing the task
    "retry_delay": timedelta(seconds=5),
    "timezone": "America/Los_Angeles",
    "depends_on_past": False,
}


with DAG(
    dag_id="earthquakes-batch-daily",
    default_args=default_args,
    schedule_interval="50 23 * * *",  # Schedule every 23:50
    catchup=True,
    max_active_runs=1,  # Set to control concurrency
    tags=["earthquakes", "daily"],  # Add the "earthquakes" tag
) as dag:

    kafka_producer = PythonOperator(
        task_id="task_kafka_producer",
        python_callable=batch,
        op_kwargs={
            "execution_date": "{{ execution_date }}"
        },  # Access execution_date from op_kwargs
        dag=dag,
    )

    pyspark_consumer = DockerOperator(
        task_id="task_pyspark_consumer",
        image="earthquakes/spark:latest",
        api_version="auto",
        auto_remove=True,
        command="./bin/spark-submit --master local[*] --packages org.postgresql:postgresql:42.5.4,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 ./pyspark_earthquakes_streaming.py",
        docker_url="tcp://docker-proxy:2375",
        environment={"SPARK_LOCAL_HOSTNAME": "localhost"},
        network_mode="airflow-kafka",
        dag=dag,
    )

    kafka_producer >> pyspark_consumer
