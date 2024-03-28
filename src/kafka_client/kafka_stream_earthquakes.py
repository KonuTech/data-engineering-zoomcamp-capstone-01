from dataclasses import dataclass, field
from typing import List, Union
from collections import Counter
import datetime
import json
import requests
import kafka.errors
from kafka import KafkaProducer
import logging


@dataclass
class EarthquakeEvent:
    # Metadata fields
    generated: int
    metadata_url: str
    metadata_title: str
    metadata_status: int
    api: str
    count: int

    # Earthquake event fields
    mag: float
    place: str
    time: int
    updated: int
    tz: Union[str, None]
    url: str
    detail: str
    felt: Union[None, int]
    cdi: Union[None, float]
    mmi: Union[None, float]
    alert: Union[None, str]
    status: str
    tsunami: int
    sig: int
    net: str
    code: str
    ids: str
    sources: str
    types: str
    nst: int
    dmin: float
    rms: float
    gap: int
    magType: str
    type: str
    title: str
    geometry_coordinates: List[float]
    # Geo fields
    longitude: float
    latitude: float
    radius: float
    id: str


def create_kafka_producer():
    """
    Creates the Kafka producer object
    """
    try:
        producer = KafkaProducer(bootstrap_servers=["kafka:9092"])
    except kafka.errors.NoBrokersAvailable:
        logging.info(
            "We assume that we are running locally, so we use localhost instead of kafka and the external "
            "port 9094"
        )
        producer = KafkaProducer(bootstrap_servers=["localhost:9094"])

    return producer

def extract_key_values(data: Union[dict, list], flattened_data: dict, parent_key: str = ''):
    """
    Recursively extract key-value pairs from nested JSON data
    and flatten them while keeping the order of dimensions intact.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                new_key = f"{parent_key}_{key}" if parent_key else key
                extract_key_values(value, flattened_data, new_key)
            else:
                new_key = f"{parent_key}_{key}" if parent_key else key
                flattened_data[new_key] = value
    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_key = f"{parent_key}_{i}" if parent_key else str(i)
            extract_key_values(item, flattened_data, new_key)

def query_earthquakes_api(params: dict) -> dict:
    base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    response = requests.get(base_url, params=params)
    return response.json()

def query_data():
    # Get the current date
    current_date = datetime.date.today().isoformat()

    params: dict = {
        "format": "geojson",
        "starttime": current_date,
        # "endtime": "2024-03-11",
        "minmagnitude": "0"
    }

    result: dict = query_earthquakes_api(params)
    features: List[dict] = result['features']
    metadata: dict = result['metadata']

    # Initialize a list to hold earthquake data
    data: List[EarthquakeEvent] = []

    for feature in features:
        properties: dict = feature['properties']
        geometry: List[float] = feature['geometry']['coordinates']

         # Extracting latitude, longitude, and radius from geometry_coordinates
        longitude = geometry[0]
        latitude = geometry[1]
        radius = geometry[2]
        
        # Initialize a data class object for the current earthquake event
        earthquake_data: EarthquakeEvent = EarthquakeEvent(
            # Metadata fields
            generated=metadata['generated'],
            metadata_url=metadata['url'],
            metadata_title=metadata['title'],
            metadata_status=metadata['status'],
            api=metadata['api'],
            count=metadata['count'],

            # Earthquake event fields
            mag=properties['mag'],
            place=properties['place'],
            time=properties['time'],
            updated=properties['updated'],
            tz=properties.get('tz'),
            url=properties['url'],
            detail=properties['detail'],
            felt=properties.get('felt'),
            cdi=properties.get('cdi'),
            mmi=properties.get('mmi'),
            alert=properties.get('alert'),
            status=properties['status'],
            tsunami=properties['tsunami'],
            sig=properties['sig'],
            net=properties['net'],
            code=properties['code'],
            ids=properties['ids'],
            sources=properties['sources'],
            types=properties['types'],
            nst=properties['nst'],
            dmin=properties['dmin'],
            rms=properties['rms'],
            gap=properties['gap'],
            magType=properties['magType'],
            type=feature['type'],
            title=properties['title'],
            geometry_coordinates=geometry,
            longitude=longitude,
            latitude=latitude,
            radius=radius,
            id=feature['id']
        )

        # Append the data class object to the list
        data.append(earthquake_data)

    # Initialize a Counter object to count unique IDs
    unique_ids = Counter()

    for event in data:
        unique_ids[event.id] += 1

    # Convert list of data class objects to JSON
    json_data = [vars(event) for event in data]

    # Display JSON data
    # for event in json_data:
    #     print(json.dumps(event))

    # Display unique IDs count
    print(f"Unique IDs Count: {len(unique_ids)}")

    return json_data

def stream():
    """
    Writes the API data to Kafka topic
    """
    producer = create_kafka_producer()
    results = query_data()

    # Send each JSON document to Kafka
    for kafka_data in results:
        producer.send("earthquakes", json.dumps(kafka_data).encode("utf-8"))

if __name__ == "__main__":
    stream()
