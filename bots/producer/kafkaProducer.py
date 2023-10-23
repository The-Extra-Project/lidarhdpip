from dotenv import load_dotenv, dotenv_values
from kafka import KafkaProducer
import time
import logging
import sys
import os
load_dotenv(dotenv_path='../../.env')
config = dotenv_values(dotenv_path='./../.env') 
logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)


global producer


producer = KafkaProducer(
  bootstrap_servers=[os.getenv("KAFKA_BROKER_URL")],
  sasl_mechanism='SCRAM-SHA-256',
  security_protocol='SASL_SSL',
  sasl_plain_password= os.getenv("SASL_PLAIN_PASSWORD"),
  sasl_plain_username= os.getenv("SASL_PLAIN_USERNAME"),
)

## kafka compute operations: 
def kafka_producer_job(Xcoord: str, Ycoord: str, username: str, ipfs_shp_file, ipfs_filename_template):
    """
    transfers the message entered by the user from the discord input to the kafka broker queue destined for bacalhau container.
    """    
    
    time.sleep(5)
    producer.send(
        topic="bacalhau_compute_job",
        key= username,
        value=(Xcoord + ',' + Ycoord +',' + username + ',' + ipfs_shp_file+ ',' + ipfs_filename_template).encode('utf-8'),
        )
    logger.log(msg="send the message to bacalhau service")
    print("Sending msg \"{} <> {} <> {} <> {} <> {}   \"".format(Xcoord, Ycoord, username, ipfs_shp_file, ipfs_filename_template)) 


def kafka_producer_polygon(coordinates: str,username: str, ipfs_shp_file, ipfs_filename_template ):
  """
  transfers the message entered by user to invoke the discord command to generate the reconstructed polygon shapefile
  coordinates: its the coagulated string of the parameters
    - for single point cropping: (X,Y), for polygon: (Xmax,Xmin,Ymax,Ymin) 
  
  
  """
  
  params = [].append(coordinates.split(','))
  
  time.sleep(5)
  producer.send(
        topic="bacalhau_compute_job",
        key= username,
        value=(params + ',' + username + ',' + ipfs_shp_file+ ',' + ipfs_filename_template).encode('utf-8'))
  
  logger.log(msg="send the message to bacalhau service")
  print("Sending msg \"{} <> {} <> {} <> {} <> {}   \"".format(params, username, ipfs_shp_file, ipfs_filename_template)) 

def kafka_produce_get_status(jobId: str, username: str):
  """
  transfers the command from discord to get the status of the given job
  jobId: is the job id corresponding to which the user has submitted the job
  """
  time.sleep(5)
  producer.send(
        topic="bacalhau_compute_job",
        key= username,
        value=(jobId +',' + username).encode('utf-8'),
        )
  
def kafka_produce_get_job_lists(username: str):
  """
    transfers the command for getting the information of jobs listed by the user 
    username: discord identifier of user
  """
  time.sleep(5)
  producer.send(
  topic="bacalhau_compute_job",
  key= username,
  value=( "job_list" + ',' + username).encode('utf-8'), ## here the job_list is just for the differentiation purposes
  )

def kafka_produce_pipeline_reconstruction(username, Xcoord, Ycoord,ipfs_shp_file, pipeline_filename, surface_reconstruction_pipeline, pathInputlasFile: str, algorithmType: int):
  """
  Passes the message in order to run the 3D reconstruction pipeline on the bacalhau job.
  """
  topic =  'bacalhau_surface_reconstruction'
  time.sleep(5)
  
  producer.send(
    "bacalhau_surface_reconstruction",
    key=username, 
    value=(username + ',' + Xcoord +','+ Ycoord +','+ ipfs_shp_file + ',' + pipeline_filename + ',' + surface_reconstruction_pipeline + ',' + algorithmType).encode('utf-8'))
  