from confluent_kafka import KafkaException
from pydantic import BaseModel
from ..kafka_config import read_ccloud_config
import uvicorn
from async_producer_template import AsyncProducer
from fastapi import FastAPI
from ..model import TwitterProducerMessage
import asyncio

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    global producer
    producer = AsyncProducer(configs=read_ccloud_config("../client.properties"))



@app.on_event("shutdown")
def shutdown_event():
    producer.close()


# def get_params(request_number: int):
#     return mappedTweets[request_number]
@app.post("/produce_tweet")
def produce_Tweet_details(tweet_params: TwitterProducerMessage):
    """
    creates a request that is stored into broker.
    """
    try:
        returnvalue = producer.produce("twitter-coord", value= tweet_params)
        return {
            "timestamp": returnvalue.timestamp()
        }
    except KafkaException as e:
        print(e)
        return HTTPException(status_code=500, detail=e.args[0].str())
    

    
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)