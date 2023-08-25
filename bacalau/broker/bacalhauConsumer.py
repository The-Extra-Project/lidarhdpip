import platform
from kafka import  KafkaConsumer
from dotenv import load_dotenv, dotenv_values
from fastapi import FastAPI
import json
import logging

from bacalau.bacalau_script import createJobBacalauPoint, listJobs , getJobResults
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

log = logging.getLogger("uvicorn")


load_dotenv(dotenv_path='../../.env')
config = dotenv_values(dotenv_path='../../.env')

app = FastAPI()

global consumer


@app.on_event("startup")
async def startup_event():
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
    
## this function is called repreatedly to consume messages from kafka
#@repeat.every()
def kafka_consume_message_jobCommand_point() -> any:
    """
    this allows for messages to be consumed that are transferred by the discord bot
    returns true if the message is consumed and the command is executed.
    """
    topic = 'bacalhau_compute_job'
    
    ## TODO: fetch the different channel name using the settings defined like in src/stashed_config
    consumer.subscribe(['bacalhau_compute_job'])
    
    
    consumer.subscribe(topic) 
   
    ## only consume the first message from the given queue.
    parameter = consumer.poll(timeout=1)
    
    logger.info('now fetching the response of corresponding key')

    [Xcoordinate, Ycoord, ipfs, dockername, username] = parameter.decode
    
    createJobBacalauPoint(Xcoordinate, Ycoord, ipfs, dockername, username)
    
    print("results of given job is:  {}{}{}".format(Xcoordinate, Ycoord, ipfs, dockername, username))
    
    

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