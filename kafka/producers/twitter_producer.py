from confluent_kafka import Producer
from pydantic import BaseModel
from ..kafka_config import read_ccloud_config
from producer_template import AsyncProducer
from fastapi import FastAPI
# stores the details of the request w/ the corresponding parameters
mappedTweets = map()

count = 0


app = FastAPI()


class tweet_responses():
    coordX: int
    coordY: int
    tweet_id: int

@app.on_event("startup")
async def startup_event():
    global producer
    producer = AsyncProducer({"bootstrap.servers": "localhost:9092"})


@app.on_event("shutdown")
def shutdown_event():
    producer.close()


def get_params(request_number: int):
    return mappedTweets[request_number]

def produce_Tweet_details(request_number: int,params: list[int]):
    """
    creates a request that is stored into the broker queue
    - client_request parameters
    - parameters in order to execute the georender: X and Y coordinates    
    """
    
    producer = Producer(read_ccloud_config("../client.properties"))
    producer.produce("tweet-producer" , key=request_number, value=params)
    count+=1
    write_params(count,params=params)
    

def write_params(request_number: int, params: list(str) ):
     mappedTweets[request_number] = params

def read_params(request_number: int):
    return mappedTweets[request_number]