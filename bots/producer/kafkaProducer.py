from dotenv import load_dotenv, dotenv_values
from kafka import KafkaProducer
import time
import logging
import sys
#from fastapi import FastAPI



load_dotenv(dotenv_path='../../.env')
config = dotenv_values(dotenv_path='../../.env')


logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)


global producer


producer = KafkaProducer(
  bootstrap_servers=[config["KAFKA_BROKER_URL"]],
  sasl_mechanism='SCRAM-SHA-256',
  security_protocol='SASL_SSL',
  sasl_plain_username=config["SASL_PLAIN_USERNAME"],
  sasl_plain_password=config["SASL_PLAIN_PASSWORD"],
)



## kafka compute operations: 
def kafka_producer_job(Xcoord: str, Ycoord: str, username: str, ipfs_shp_file, ipfs_filename_template):
    """
    transfers the message entered by the user from the discord input to the kafka broker queue destined for bacalhau container.
    message: the coordinates of the possition that the georender compute application will take as the parameter.
    """    
    
    time.sleep(5)
    result = producer.send(
        topic="bacalhau_compute_job",
        key= username
        value=(Xcoord + ',' + Ycoord +',' + username + ',' + ipfs_shp_file+ ',' + ipfs_filename_template).encode('utf-8'),
        )
    logger.log(msg="send the message to bacalhau service")
    print("Sending msg \"{} <> {} <> {} <> {} <> {}   \"".format(Xcoord, Ycoord, username, ipfs_shp_file, ipfs_filename_template)) 
