from confluent_kafka import Producer, KafkaError
from ..web3Storage import API 
import json
from ..kafka_config import read_ccloud_config

web3Storage = API('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDZENUE1NmQxYTFEZDAzYmFhZjkyQTUwOTA1NzIwQWJmMDdkOTQzQkEiLCJpc3MiOiJ3ZWIzLXN0b3JhZ2UiLCJpYXQiOjE2ODI1ODUzMDgxMzgsIm5hbWUiOiJleHRyYS1jb21tdW5pdHktQVBJIn0.CW_1s8nBQwb-GZF_R4SPI4NQsKP7KETuaGRssAkekTc')


## schema for the producer: client_id, image_url and metadata.

def requestDestinationStorage(clientImageName: str, clintId: str):
    """
    this producer command submits the requests once the georender has generated the geospatial image from the geo-coordinates
    """
    producer = Producer(read_ccloud_config("../client.properties"))
    producer.produce("web3-storage-production" , key=clintId, value=clientImageName)






