from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime

from src.kafka_client.kafka_earthquakes_minibatch_five import minibatch


start_date = datetime.today() - timedelta(minutes=10)

default_args = {
    "owner": "airflow",
    "start_date": start_date,
    "retries": 2,  # number of retries before failing the task
    "retry_delay": timedelta(seconds=5),
    'timezone': 'America/Los_Angeles'
}


with DAG(
    dag_id="earthquakes-minibatch-5",
    default_args=default_args,
    schedule_interval='*/5 * * * *',  # Schedule every 5 minutes
    catchup=True,
    max_active_runs=1,  # Set to control concurrency
    tags=["earthquakes", "minutes"]  # Add the "earthquakes" tag
) as dag:


    kafka_producer = PythonOperator(
        task_id="task_kafka_producer",
        python_callable=minibatch,
        op_kwargs={'execution_date': '{{ execution_date }}'},  # Access execution_date from op_kwargs
        dag=dag,
    )


    pyspark_consumer = DockerOperator(
        task_id="task_pyspark_consumer",
        image="earthquakes/spark:latest",
        api_version="auto",
        auto_remove=True,
        command="./bin/spark-submit --master local[*] --packages org.postgresql:postgresql:42.5.4,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 ./pyspark_earthquakes_streaming.py",
        docker_url='tcp://docker-proxy:2375',
        environment={'SPARK_LOCAL_HOSTNAME': 'localhost'},
        network_mode="airflow-kafka",
        dag=dag,
    )


    kafka_producer >> pyspark_consumer
