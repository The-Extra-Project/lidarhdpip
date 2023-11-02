import platform
from kafka import  KafkaConsumer
from dotenv import load_dotenv, dotenv_values
from fastapi import FastAPI, BackgroundTasks
#from bacalau_script import createJobBacalauPoint, listJobs , getJobResults
import uvicorn
from fastapi_scheduler import SchedulerAdmin
import json
import logging
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)



log = logging.getLogger("uvicorn")

app = FastAPI()

admin = AdminSite(settings=Settings(database_url="sqlite+aiosqlite:///trigger.db"))
admin.mount_app(app)

scheduler = SchedulerAdmin.bind(admin)


load_dotenv(dotenv_path='../../.env')

global consumer
 

consumer = KafkaConsumer(
          bootstrap_servers=[os.getenv("KAFKA_BROKER_URL")],
  sasl_mechanism='SCRAM-SHA-256',
  security_protocol='SASL_SSL',
  sasl_plain_username=os.getenv("SASL_PLAIN_USERNAME"),
  sasl_plain_password=os.getenv("SASL_PLAIN_PASSWORD"),
        auto_offset_reset='earliest',
        consumer_timeout_ms=1000
    )
    
## this function is called repreatedly to consume messages from kafka (i.e user commands)
@scheduler.scheduled_job('interval', seconds=120)
def kafka_consume_message_jobCommand_point() -> any:
    """
    this allows for messages to be consumed that are transferred by the discord bot
    returns true if the message is consumed and the command is executed.
    """
    topic = 'bacalhau_compute_job'
    
    ## TODO: fetch the different channel name using the settings defined like in src/stashed_config
    consumer.subscribe(['bacalhau_compute_job'])
    
    ## only consume the first message from the given queue.
    parameter = consumer.poll(timeout_ms=100)
    
    logger.info('now fetching the response of corresponding key')

    # now parsing the parameter key and return all the values
    
    [Xcoordinate, Ycoord, ipfs, dockername, username] = parameter
    
#    submit_spec = createJobBacalauPoint(Xcoordinate, Ycoord, ipfs, dockername, username)
    
    print("job has started for:  {}{}{}".format(Xcoordinate, Ycoord, ipfs, dockername, username))
    

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
    
    
    
    
test = True

if __name__ == "__main__":
    uvicorn.run(host="127.0.0.1", port=8000)
