import platform
from kafka import  KafkaConsumer
from dotenv import load_dotenv, dotenv_values
#from fastapi import FastAPI
import json
import logging

import time


import json
logger = logging.getLogger()
logger.setLevel(logging.INFO)
log = logging.getLogger("uvicorn")


load_dotenv(dotenv_path='../../.env')
config = dotenv_values(dotenv_path='../../.env')

consumer: KafkaConsumer

async def startup_event(self):
    """Start up event for FastAPI application."""

    log.info("Starting up consumer")
    consumer = KafkaConsumer(
          bootstrap_servers=[config["KAFKA_BROKER_URL"]],
  sasl_mechanism='SCRAM-SHA-256',
  security_protocol='SASL_SSL',
  sasl_plain_username=config["SASL_PLAIN_USERNAME"],
  sasl_plain_password=config["SASL_PLAIN_PASSWORD"],
        auto_offset_reset='earliest',
        consumer_timeout_ms=1000
    )
    
def kafka_consume_message_jobResult(self,topic: str, keyID: str) -> json:
    """
    this allows for messages to be consumed that is shared by the bacalhau storing the response to the job status function.
    keyID corresponds to which of you wanted  get the job response (this will be either jobId or based on user details)
    """
    topic = 'bacalhau_compute_job'
    
    consumer.subscribe(topic) 
    logger.info('now fetching the response of keyID provided by the user')
    ## only consider last message for consuming for bacalhau 
    
    for message in consumer:
        if(message[keyID].key == keyID):
            current_message_offset = message[keyID].value
            break
        
    consumer.seek(partition=topic, offset=current_message_offset)
    
    parameters = json.loads(consumer.poll(topic))
    [cid, nodeId, path] = parameters
    
    print("results of given job is:  {}{}{}".format(cid,nodeId,path))

def kafka_consume_result_status(keyID: str):
    topic = 'bacalau_list_jobs'
    
    consumer.subscribe(topic) 
    logger.info('now fetching the response of keyID provided by the user')
    
    for message in consumer:
        if(message[keyID].key == keyID):
            current_message_offset = message[keyID].value
            break
        
    consumer.seek(partition=topic, offset=current_message_offset)
    
    parameters = json.loads(consumer.poll(topic))
    [cid, nodeId, path] = parameters
