from confluent_kafka import  KafkaConsumer, Consumer
from ..kafka_config import read_ccloud_config
from  fastapi import FastAPI, HTTPException
import requests
import time
from pydantic import BaseModel




group_name = "web3-twitter"


params = read_ccloud_config('../client.properties')
bootstrap_servers = params["Bootstrap server"]



def parse_requests_bot(topic, Consumer):


# def main():

#     consumer = KafkaConsumer(
#         topic_name,
#         bootstrap_servers=[bootstrap_servers],
#         auto_offset_reset='latest',
#         enable_auto_commit=True,
#         auto_commit_interval_ms =  5000,
#         fetch_max_bytes = 128,
#         max_poll_records = 100,
#         )

#     for message in consumer:
#         #TODO: call the api method of bacalau with the 
#         ## deserialize the consumed messages
#         print(message.value)
#         createJobCoordinate(params, "lxet/georender_bacalau","test")
        

# if __name__ == "__main__":
#     main()



    