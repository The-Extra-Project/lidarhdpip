from dotenv import load_dotenv, dotenv_values
from kafka import KafkaProducer
import time
import logging
import sys
from fastapi_scheduler import SchedulerAdmin
from fastapi import FastAPI

load_dotenv(dotenv_path='../../.env')
config = dotenv_values(dotenv_path='../../.env')

logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)

app = FastAPI()

scheduler = SchedulerAdmin.bind(app)

global producer

producer = KafkaProducer(
  bootstrap_servers=[config["KAFKA_BROKER_URL"]],
  sasl_mechanism='SCRAM-SHA-256',
  security_protocol='SASL_SSL',
  sasl_plain_username=config["SASL_PLAIN_USERNAME"],
  sasl_plain_password=config["SASL_PLAIN_PASSWORD"],
)


## kafka compute operations result: 
@scheduler.scheduled_job(trigger='interval', seconds=120)
def kafka_producer_Job_result():
    """
    returns the result to the given user georendered job from bacalau script.
    it takes the output of the resulting user jobID that is generated from the bacalhau consumer call of application
    """    
    ## fetching the latest job result if available
    if (listJobs):
        jobId = listJobs()['-1']

    jobResult = getJobResults(jobId)

    logger.info("Sending Job Result to Kafka Topic")
    
    time.sleep(5)
    result = producer.send(
        topic="bacalhau_compute_job",
        value=  JobResults.encode('utf-8'),
        )
    logger.info("send the message to bacalhau service")
    print("Sending msg \"{}\"".format(result))
    
    return True

def kafka_produce_list_jobs():
    jobLists = listJobs()
    logger.info("Sending Job Lists to Kafka Topic")
    transfer = producer.send(
        topic="bacalau_result_job",
        value= jobLists.encode('utf-8'),
    )
    logger.info("Send the resulting jobs to the broker of format: {}, with id:".format(transfer))
    
