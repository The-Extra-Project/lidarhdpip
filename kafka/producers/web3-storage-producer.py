from confluent_kafka import Producer, KafkaException
from web3storage import API 
from ..kafka_config import read_ccloud_config
from fastapi import FastAPI
from configparser import ConfigParser
from fastapi import FastAPI
import uvicorn


import json
from ..kafka_config import read_ccloud_config

app = FastAPI()

# get enviornment variables 
web3Storage = API()

global producer
producer = Producer(read_ccloud_config("../client.properties"))
## schema for the producer: client_id, image_url and metadata.


@app.post("/storage/{clientId}/{cid_value}")
def requestDestinationStorage(cid_value: str, clientId: str):
    """
    This producer command submits the requests once the georender has generated the geospatial image from the geo-coordinates
    cid_value: is the value of the registered of the image. 
    """
    
    try:
        producer.produce("web3-storage-production" , key=clientId, value=cid_value)
    except KafkaException as e:
        print(e)
    

def initStorageProducer(clientId: str) -> str:
    """
    store image generated from the computation 
    
    clientId: is the unique identifier (twitter username).
    return: the cid value of the image.
    """
    try:
        producer.produce("web3-init-production", key= clientId)
    except KafkaException as e:
        print(e)


if __name__ == "__main__":
     uvicorn.run(app, host="0.0.0.0", port=8001)









