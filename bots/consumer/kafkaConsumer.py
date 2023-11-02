import platform
from kafka import  KafkaConsumer
from dotenv import load_dotenv, dotenv_values
import json
import logging
import os
import time


import json
logger = logging.getLogger()
logger.setLevel(logging.INFO)
log = logging.getLogger("uvicorn")


load_dotenv(dotenv_path='../../.env')

consumer: KafkaConsumer

consumer = KafkaConsumer(
    bootstrap_servers=[os.getenv("KAFKA_BROKER_URL")],
    sasl_mechanism='SCRAM-SHA-256',
    security_protocol='SASL_SSL',
    sasl_plain_username=os.getenv("SASL_PLAIN_USERNAME"),
    sasl_plain_password=os.getenv("SASL_PLAIN_PASSWORD"),
    )
    
async def kafka_consume_message_jobResult(topic: str, keyID: str):
    """
    this allows for messages to be consumed that is shared by the bacalhau storing the response to the job status function.
    keyID corresponds to which of you wanted  get the job response (this will be either jobId or based on user details)
    """
    
    consumer.subscribe([topic]) 
    logger.info('now fetching the response of keyID provided by the user')
    ## only consider last message for consuming for bacalhau 
    
    # for message in consumer:
    #     if message.key.decode('utf-8') == keyID:
    #         print("values" + message.value)
    #     consumer.poll(timeout_ms=100)
    #     consumer.commit()
        
    
    parameters = consumer.poll(timeout_ms=100)
    consumer.commit()

    print("results of given job is:  {}".format(parameters))

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
