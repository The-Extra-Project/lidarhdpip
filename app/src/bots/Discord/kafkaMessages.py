from dotenv import load_dotenv, dotenv_values
import logging
import platform
from kafka import KafkaProducer, KafkaConsumer
import os
import random
import asyncio
import Commands
load_dotenv(dotenv_path='../../.env')

config = dotenv_values(dotenv_path='../../.env')


logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)


global producer
global consumer
producer = KafkaProducer(
  bootstrap_servers=[config["KAFKA_BROKER_URL"]],
  sasl_mechanism='SCRAM-SHA-256',
  security_protocol='SASL_SSL',
  sasl_plain_username=config["SASL_PLAIN_USERNAME"],
  sasl_plain_password=config["SASL_PLAIN_PASSWORD"],
)

consumer = KafkaConsumer(
          bootstrap_servers=[config["KAFKA_BROKER_URL"]],
  sasl_mechanism='SCRAM-SHA-256',
  security_protocol='SASL_SSL',
  sasl_plain_username=config["SASL_PLAIN_USERNAME"],
  sasl_plain_password=config["SASL_PLAIN_PASSWORD"],
        auto_offset_reset='earliest',
        consumer_timeout_ms=1000
    )
    



## kafka compute operations: 
def kafka_producer_message(Xcoord: str, Ycoord: str, username: str):
    """
    transfers the message entered by the user from the discord input to the kafka broker queue destined for bacalhau computation.
    message: the coordinates of the possition that the georender compute application will take as the parameter.
    """    
    
    
    result = producer.send(
        topic="bacalhau_compute_job",
        value=(Xcoord + ',' + Ycoord +',' + username).encode('utf-8'),
        )
    print("Sending msg \"{},{}\"".format(Xcoord, Ycoord))
    print(result)
    return True

    
def kafka_consumer():
    """
    This function will fetch the messages from the broker queue that are essentially the results from the bacalhau node, 
    read the message and then prints the result.
    
    TODO: this fn will be shifted to the georender along w/ allowing threading process """
    
    consumer.subscribe(['bacalhau_compute_job'])
    
    
    for msg in consumer:
        print(msg)
    producer.flush()
    producer.close()
    consumer.close()
