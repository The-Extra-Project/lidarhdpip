from dotenv import load_dotenv, dotenv_values
from kafka import KafkaProducer
from kafka.errors import KafkaError
import time
import logging
import sys
from kafka.producer import future

load_dotenv(dotenv_path='.env')
config = dotenv_values(dotenv_path='.env')


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
def kafka_producer_mock_job_message(
    Xcoord: str, Ycoord: str, username: str, ipfs_template_cid: str, ipfs_pipeline_cid: str
):
    """
    mocks the messaging from the discord bot to kafka broker.
    """    

    try:
        result: KafkaProducer.send = producer.send(
                topic="bacalhau_compute_job",
                value=(Xcoord + ',' + Ycoord +',' + username + ',' + ipfs_pipeline_cid + ','+ ipfs_template_cid).encode('utf-8'),
                key= bytes(counter)
                )
        print("send the message to bacalhau service")
        print("Sending msg \"{}\"".format(result))
    except KafkaError as k:
            print(k)

    counter = 0
    return True

    
if __name__ == '__main__':
    kafka_producer_mock_job_message()
    