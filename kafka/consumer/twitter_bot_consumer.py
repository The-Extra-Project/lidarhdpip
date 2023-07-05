from confluent_kafka import  KafkaConsumer, Consumer
from ..kafka_config import read_ccloud_config
from  fastapi import FastAPI, HTTPException
import requests
import time
from pydantic import BaseModel
from confluent_kafka.error import ConsumeError, KafkaException
import uvicorn

app = FastAPI()




@app.on_event("startup")
async def startup_event():
    global consumer
    consumer = Consumer(configs=read_ccloud_config("../client.properties"))



@app.on_event("shutdown")
def shutdown_event():
    consumer.close()


topic_name = "tweet-coord"


params = read_ccloud_config('../client.properties')
bootstrap_servers = params["Bootstrap server"]

@app.get("/consume_tweet")
def parse_requests_bot(topic, Consumer):
    """
    this function consumes the messages generated in the queue , and then calls the 
    write_tweets function.

    """
    try:
        consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=[bootstrap_servers],
        auto_offset_reset='latest',
        )

        for message in consumer:
            #TODO: call the api method of bacalau with the 
            ## deserialize the consumed messages
            print(message.value)
#         createJobCoordinate(params, "lxet/georender_bacalau","test")

    except KafkaException as k:
        print(k)
    


if __name__ == "__main__":
     uvicorn.run(app, host="0.0.0.0", port=8001)