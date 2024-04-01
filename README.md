# [Plug & Play] Earthquakes - minibatch 
## Objective

This repository contains the final project for the [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) course provided by [DataTalks.Club](https://datatalks.club/).

The goal of the project is to apply what we have learned during the course. This project aims to develop an exemplary data pipeline using [Apache Airflow](https://airflow.apache.org/docs/apache-airflow/stable/index.html) for [Apache Kafka](https://kafka-python.readthedocs.io/en/master/), [PySpark](https://spark.apache.org/docs/latest/api/python/index.html), and [PostgreSQL](https://www.postgresql.org/). High level perspective of project's architecture is shown on a below diagram.

<img src="static/diagram_architecture.png" width="60%"/>

## Data source

The data being used for this project comes from a publicly available provider, namely, the U.S. Geological Survey (USGS). The USGS, as outlined on its 'About Us' page, serves as the science arm of the Department of the Interior, offering a diverse range of earth, water, biological, and mapping data and expertise to support decision-making on environmental, resource, and public safety issues. Established by an act of Congress in 1879, the USGS continuously adapts its scientific endeavors to address the evolving needs of society.

Aligned with its mission, the USGS provides access to an Application Programming Interface (API) that offers information about the history of earthquakes, free of charge. This API facilitates access to up-to-date earthquake data, including recent events. For specific details regarding the frequency of earthquake data updates, please refer to the relevant [page](https://www.usgs.gov/faqs/how-quickly-earthquake-information-posted-usgs-website-and-sent-out-earthquake-notification) on the USGS website.


The data being used for this project comes from a publicly available provider, namely, the U.S. Geological Survey (USGS). The USGS, as outlined on its 'About Us' page, serves as the science arm of the Department of the Interior, offering a diverse range of earth, water, biological, and mapping data and expertise to support decision-making on environmental, resource, and public safety issues. Established by an act of Congress in 1879, the USGS continuously adapts its scientific endeavors to address the evolving needs of society.

Aligned with its mission, the USGS provides access to an Application Programming Interface (API) that offers information about the history of earthquakes, free of charge. This API facilitates access to up-to-date earthquake data, including recent events. For specific details regarding the frequency of earthquake data updates, please refer to the relevant page on the USGS website.

The convenience of the data being updated quite frequently aligns with my concept for the development of a so-called minibatch data pipeline. As previously mentioned, data is retrieved via API using Apache Kafka, transformed using PySpark, and ingested into a PostgreSQL table. Ultimately, this data is visualized using Streamlit, contributing to a comprehensive analysis and understanding of seismic activity trends.

In addition to the described data pipeline components, two separate Airflow Directed Acyclic Graphs (DAGs) are utilized. The first DAG operates on a minibatch basis with a 5-minute interval, while the second DAG is a daily batch process.

The minibatch DAG orchestrates the retrieval of seismic data at a regular 5-minute interval. This interval-based approach ensures near-real-time ingestion of recent earthquake events into the pipeline. Each minibatch of data is processed and transformed before being ingested into the designated PostgreSQL table.

Meanwhile, the daily DAG is responsible for monitoring and handling potential late entries that may have been missed during the day. This DAG performs a daily check to identify any such late entries and appends them to the same PostgreSQL table used for the minibatch data. By consolidating these late entries with the regular minibatch data, the pipeline ensures comprehensive and up-to-date seismic data records within a single table.

Overall, these two Airflow DAGs work in tandem to maintain the integrity and timeliness of seismic data ingestion, offering a robust solution for continuous data processing and analysis.

## Training

The experiments conducted resulted in several different training runs, using various architectures of CNNs (convolutional neural networks). Various versions of pre-trained models were employed in the hope of improving the quality of the champion model. The impact of so-called Transfer Learning can be observed both [here](https://github.com/KonuTech/machine-learning-zoomcamp-capstone-02/blob/main/notebooks/02_get_champion_binary_classifier.ipynb) and on [Kaggle](https://www.kaggle.com/code/konutech/machine-learning-zoomcamp-pizza-classifier/notebook), where you can run the notebook responsible for training the champion model yourself.

The list of pre-trained models used in experiments where transfer learning approach was applied:
* Xception
* EfficientNetB3
* InceptionV3
* EfficientNetB5
* VGG16

## Model deployment and serving

The model was first tested as a containerized Flask app. Afterwards, the model was served as a Kind Kubernetes cluster. To see how to apply the model, look into the details below.

### Applied technologies

| Name             | Scope                             | Description                                                                                                            |
| ----------------| ---------------------------------| ---------------------------------------------------------------------------------------------------------------------- |
| Docker Desktop   | Continuous integration, local development, containerization         | Docker Desktop is a platform that enables the development, shipping, and running of applications within containers. It is utilized for tasks such as exploratory data analysis (EDA), conducting experiments, and model scoring. |
| Apache Airflow  | Workflow orchestration, automation, task scheduling, monitoring | Apache Airflow is an open-source platform used for programmatically authoring, scheduling, and monitoring workflows. It is particularly valuable for tasks including pre-processing, feature engineering, transfer learning, and model serving. |
| Apache Kafka    | web service                       | Apache Kafka is a distributed event streaming platform, commonly employed for building real-time streaming data pipelines and web services. |
| PySpark          | Data transformation, and analytics       | PySpark is a Python library that provides APIs for performing large-scale data processing and analysis, especially suitable for parallel and distributed computing tasks. |
| PostgreSQL      | RDBMS                              | PostgreSQL is an open-source relational database management system (RDBMS) known for its reliability, robustness, and extensive feature set, commonly used for storing structured data. |
| Streamlit       | web service                        | Streamlit is an open-source app framework designed for creating custom web applications tailored for machine learning and data science projects, facilitating easy deployment and sharing of data-driven applications. |
| black           | Python code formatting            | black is a Python code formatter that ensures a consistent and readable code style by applying strict rules automatically during code formatting processes. |
| isort           | Python import sorting             | isort is a Python library used for sorting Python imports within a file, ensuring a consistent and organized import order according to predefined configuration settings. |

Project Structure
------------
    ├── data
    │   ├── pizza_not_pizza
    │   ├── not_pizza
    │   ├── pizza
    ├── k8s
    │   ├── pizza-model
    │   │   ├── assets
    │   │   ├── variables
    ├── models
    ├── notebooks
    │   ├── training_logs
    │   │   ├── pizza_classification
    │   │   │   │   ├── 20240106-175439
    │   │   │   │   ├── train
    │   │   │   │   ├── validation
    |   │   │   │   ├── 20240106-181636
    │   │   │   │   ├── train
    │   │   │   │   ├── validation
    |
    |
    |
    ├── scoring
    │   ├── logs
    │   ├── models

## Reproducibility

##### Pre-requisties

* python 3.9 or above
* Docker Desktop, Kind, kubectl
* pip3, pipenv
* git-lfs

### Docker deployment (containerization)
Before deploying to a Kubernetes cluster, the model was tested locally using Docker Compose. For this purpose, a Dockerfile was employed. The content of the [Dockerfile](https://github.com/KonuTech/machine-learning-zoomcamp-capstone-02/blob/main/scoring/Dockerfile) defines the configuration of a service. Additionally, a script named [predict_test.py](https://github.com/KonuTech/machine-learning-zoomcamp-capstone-02/blob/main/scoring/predict_test.py) is used to test predictions. This script is stored locally and passes a URL with an image of one's choice to [predict.py](). The latter is stored in a container along with a copy of a TensorFlow model.

Once in ./scoring directory - where [Dockerfile](https://github.com/KonuTech/machine-learning-zoomcamp-capstone-02/blob/main/scoring/Dockerfile) is present - you can build up the image with:
```
$ docker build -t machine-learning-zoomcamp-capstone-02 .
[+] Building 120.4s (13/13) FINISHED                                                                                                                                                                                docker:default 
 => [internal] load .dockerignore                                                                                                                                                                                             0.1s 
 => => transferring context: 2B                                                                                                                                                                                               0.0s 
 => [internal] load build definition from Dockerfile                                                                                                                                                                          0.1s 
 => => transferring dockerfile: 389B                                                                                                                                                                                          0.0s 
 => [internal] load metadata for docker.io/library/python:3.9.3-slim                                                                                                                                                          2.4s 
 => [1/8] FROM docker.io/library/python:3.9.3-slim@sha256:3edfa765f8f77f333c50222b14552d0d0fa9f46659c1ead5f4fd10bf96178d3e                                                                                                    0.0s 
 => [internal] load build context                                                                                                                                                                                             0.0s 
 => => transferring context: 2.98kB                                                                                                                                                                                           0.0s 
 => CACHED [2/8] RUN pip install pipenv                                                                                                                                                                                       0.0s 
 => CACHED [3/8] WORKDIR /app                                                                                                                                                                                                 0.0s 
 => [4/8] COPY [predict.py, Pipfile, Pipfile.lock, ./]                                                                                                                                                                        0.1s 
 => [5/8] RUN pipenv install --system --deploy                                                                                                                                                                              106.8s 
 => [6/8] RUN mkdir models                                                                                                                                                                                                    0.6s
 => [7/8] RUN mkdir logs                                                                                                                                                                                                      0.7s
 => [8/8] COPY [models/model_xception_2024-01-06_22-44-37.keras, models/]                                                                                                                                                     0.8s
 => exporting to image                                                                                                                                                                                                        8.6s
 => => exporting layers                                                                                                                                                                                                       8.6s
 => => writing image sha256:647e632aaf90f351add90a802284d99447063eaa62e454df07223aa86f21d60e                                                                                                                                  0.0s
 => => naming to docker.io/library/machine-learning-zoomcamp-capstone-02                                                                                                                                                      0.0s
```
After successful build of image you can run the Flask app stored iside it:
```
$ docker run -it --rm -p 6969:6969 --entrypoint=bash machine-learning-zoomcamp-capstone-02
root@0da539eb1ed1:/app#

root@5caec8e9b5fb:/app# ls
Pipfile  Pipfile.lock  logs  models  predict.py

root@0da539eb1ed1:/app# python predict.py
2024-01-13 21:31:57.584757: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'libcudart.so.11.0'; dlerror: libcudart.so.11.0: cannot open shared object file: No such file or directory
2024-01-13 21:31:57.584810: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2024-01-13 21:31:58.884489: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'libcuda.so.1'; dlerror: libcuda.so.1: cannot open shared object file: No such file or directory
2024-01-13 21:31:58.884542: W tensorflow/stream_executor/cuda/cuda_driver.cc:269] failed call to cuInit: UNKNOWN ERROR (303)
2024-01-13 21:31:58.884593: I tensorflow/stream_executor/cuda/cuda_diagnostics.cc:156] kernel driver does not appear to be running on this host (0da539eb1ed1): /proc/driver/nvidia/version does not exist
2024-01-13 21:31:58.884803: I tensorflow/core/platform/cpu_feature_guard.cc:151] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX2 FMA
To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
 * Serving Flask app 'predict'
 * Debug mode: on
2024-01-13 21:32:00.626125: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'libcudart.so.11.0'; dlerror: libcudart.so.11.0: cannot open shared object file: No such file or directory
2024-01-13 21:32:00.626184: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2024-01-13 21:32:01.796997: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'libcuda.so.1'; dlerror: libcuda.so.1: cannot open shared object file: No such file or directory
2024-01-13 21:32:01.797050: W tensorflow/stream_executor/cuda/cuda_driver.cc:269] failed call to cuInit: UNKNOWN ERROR (303)
2024-01-13 21:32:01.797097: I tensorflow/stream_executor/cuda/cuda_diagnostics.cc:156] kernel driver does not appear to be running on this host (0da539eb1ed1): /proc/driver/nvidia/version does not exist
2024-01-13 21:32:01.797293: I tensorflow/core/platform/cpu_feature_guard.cc:151] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX2 FMA
To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
```
##### Testing with python script
Now from local terminal we can run:
```
KonuTech@DESKTOP-D7SFLUT MINGW64 ~/machine-learning-zoomcamp-capstone-02 (main)
$ python scoring/predict_test.py
```
To see that containerized prediction app returend:
```
2024-01-13 21:32:01.797293: I tensorflow/core/platform/cpu_feature_guard.cc:151] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX2 FMA
To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
It is a pizza!
```
<img src="static/it_is_a_pizza_docker.jpg" width="80%"/>

##### Dependencies
The list of dependencies for a deployment using Docker is available [here](https://github.com/KonuTech/machine-learning-zoomcamp-capstone-02/blob/main/scoring/Pipfile). These dependencies are installed during the build of the Docker image.
### Kind deployment (Kubernetes)
We are going to use the tool [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/) to create a Kubernetes cluster locally. A single pod is created for each of the services: one pod for a model-serving service and another pod for the creation of a so-called gateway. This is illustrated in the architecture schema image shown previously.

Here, I am assuming that you were already able to install [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/). 
##### Dependencies
The list of dependencies for successful deployment of Kind cluster locally is available [here](https://github.com/KonuTech/machine-learning-zoomcamp-capstone-02/blob/main/k8s/Pipfile). The Pipefile is used during build of [pizza-gateway.dockerfile](https://github.com/KonuTech/machine-learning-zoomcamp-capstone-02/blob/main/k8s/pizza-gateway.dockerfile) image.
##### Prerequisites

If you are a Windows user you can download Kind using following URL:

```
curl.exe -Lo kind-windows-amd64.exe https://kind.sigs.k8s.io/dl/v0.20.0/kind-windows-amd64
Move-Item .\kind-windows-amd64.exe c:\kind\kind.exe
```

Next you can create a cluster with:
```
PS C:\kind> .\kind.exe create cluster
```
You should see:
```
Creating cluster "kind" ...
 • Ensuring node image (kindest/node:v1.27.3) 🖼  ...
 ✓ Ensuring node image (kindest/node:v1.27.3) 🖼
 • Preparing nodes 📦   ...
 ✓ Preparing nodes 📦
 • Writing configuration 📜  ...
 ✓ Writing configuration 📜
 • Starting control-plane 🕹️  ...
 ✓ Starting control-plane 🕹️
 • Installing CNI 🔌  ...
 ✓ Installing CNI 🔌
 • Installing StorageClass 💾  ...
 ✓ Installing StorageClass 💾
Set kubectl context to "kind-kind"
You can now use your cluster with:

kubectl cluster-info --context kind-kind

Thanks for using kind! 😊
```
Check if cluster is up and running with:
```
PS C:\kind> kubectl cluster-info --context kind-kind
```
You should see something like following:
```
Kubernetes control plane is running at https://127.0.0.1:59542
CoreDNS is running at https://127.0.0.1:59542/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```
Now you can create bunch of Docker images:
```
docker build -t machine-learning-zoomcamp-capstone-02:xception-001 \
    -f pizza-model.dockerfile .

docker build -t machine-learning-zoomcamp-capstone-02-gateway:001 \
    -f pizza-gateway.dockerfile .
```
Next, load previously created and tested Docker images into the cluster:
```
C:\kind>kind load docker-image machine-learning-zoomcamp-capstone-02:xception-001
Image: "machine-learning-zoomcamp-capstone-02:xception-001" with ID "sha256:5e45971598ba189a7bd5f36a182a2e27272303a35a498cfa0a2574ba357e8ffd" not yet present on node "kind-control-plane", loading...

C:\kind>.\kind.exe load docker-image machine-learning-zoomcamp-capstone-02-gateway:001
Image: "machine-learning-zoomcamp-capstone-02-gateway:001" with ID "sha256:8168d041ad2e8d9f0c227fd5b9b56e1db4236c6e8766cc094d086866fa66e480" not yet present on node "kind-control-plane", loading...
```
Now, we can create resources from .yaml files:
```
$ kubectl apply -f model-deployment.yaml
deployment.apps/tf-serving-pizza-model created

$ kubectl apply -f gateway-deployment.yaml
deployment.apps/gateway created

$ kubectl apply -f model-service.yaml
service/tf-serving-pizza-model created

kubectl apply -f gateway-service.yaml
deployment.apps/gateway created
```
We can check any running pod or service:
```
$ kubectl get pod
NAME                                     READY   STATUS    RESTARTS        AGE
gateway-549c6cb9bc-bszf8                 1/1     Running   5 (3h14m ago)   3d23h
tf-serving-pizza-model-c956959f9-rdhqv   1/1     Running   5 (3h14m ago)   4d1h

$ kubectl get services
NAME                     TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
gateway                  LoadBalancer   10.96.189.170   <pending>     80:30322/TCP   3d23h
kubernetes               ClusterIP      10.96.0.1       <none>        443/TCP        40d
tf-serving-pizza-model   ClusterIP      10.96.115.145   <none>        8500/TCP       4d1h
```
The last thing to do is to forward ports:
```
kubectl port-forward tf-serving-pizza-model-c956959f9-rdhqv 8500:8500
kubectl port-forward gateway-549c6cb9bc-bszf8 9696:9696
kubectl port-forward service/gateway 8080:80
```

##### Testing with python script
Now, since the ports were forwared we can try to make a prediction:
```
python k8s/predict_test.py
```
After that we can confirm if the prediction was done thanks to the log from the gateway:
```
$ kubectl logs gateway-549c6cb9bc-bszf8
[2024-01-13 08:59:42 +0000] [1] [INFO] Starting gunicorn 21.2.0
[2024-01-13 08:59:42 +0000] [1] [INFO] Listening at: http://0.0.0.0:9696 (1)
[2024-01-13 08:59:42 +0000] [1] [INFO] Using worker: sync
[2024-01-13 08:59:42 +0000] [10] [INFO] Booting worker with pid: 10
2024-01-13 08:59:44.013754: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'libcudart.so.11.0'; dlerror: libcudart.so.11.0: cannot open shared object file: No such file or directory
2024-01-13 08:59:44.013866: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
2024-01-13 12:15:29,210 - DEBUG - Received URL for prediction: https://m.kafeteria.pl/shutterstock-84904912-9cb8cae338,730,0,0,0.jpg
2024-01-13 12:15:29,482 - DEBUG - Sending prediction request to TensorFlow Serving.
2024-01-13 12:15:30,713 - DEBUG - Received prediction response from TensorFlow Serving.
2024-01-13 12:15:30,713 - DEBUG - Prediction result: It's a pizza!
```
<img src="static/it_is_a_pizza_cluster.jpg" width="80%"/>


### Peer review criterias - a self assassment:
* Problem description
    * 4 points: Problem is well described and it's clear what the problem the project solves
* Cloud
    * 0 points: Cloud is not used, things run only locally
* Data ingestion (choose either batch or stream)
    * Batch / Workflow orchestration
        * 4 points: End-to-end pipeline: multiple steps in the DAG, uploading data to data lake
* Data warehouse
    * 0 points: No DWH is used
    * 2 points: Tables are created in DWH, but not optimized
* Transformations (dbt, spark, etc)
    * 4 points: Tranformations are defined with dbt, Spark or similar technologies
* Dashboard
    * 0 points: No dashboard
    * 2 points: A dashboard with 1 tile
    * 4 points: A dashboard with 2 tiles
* Reproducibility
    * 4 points: Instructions are clear, it's easy to run the code, and the code works
