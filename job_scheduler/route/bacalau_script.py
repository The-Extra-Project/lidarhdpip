"""
This script interacts with the API gateway to
- submit the job for the pipeline reconstruction.
- get the status of the jobs submited by the given username.
""" 
from fastapi import  APIRouter, Request, Response, status
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv, dotenv_values

import boto3
import json
import os
import logging
import requests

from bacalhau_apiclient.models.storage_spec import StorageSpec
from bacalhau_sdk.api import submit
from bacalhau_sdk.config import get_client_id
from bacalhau_sdk.api import results, states
from dotenv import dotenv_values
from fastapi_scheduler import SchedulerAdmin
from kafka import KafkaConsumer
logging.getLogger('boto3').setLevel(logging.CRITICAL)
config = dotenv_values(dotenv_path='.env')

client = boto3.client('ecs', region_name='us-east-1', aws_secret_access_key=os.getenv("SECRET_KEY_AWS"))
api_client = boto3.client('apigateway', region_name="us-east-1")

router = APIRouter(
    prefix="/jobs",
    tags=["bot-service"],
    responses={404: {"description": "Not found"}},
)
## runs the cron job on the kafka routing for fetching the result 
scheduler = SchedulerAdmin.bind(router)

load_dotenv(dotenv_path='./../.env')






def cron_job(topic_name: str):
    """
    this function runs the loop job in fetching the kafka topic messages in order to get the parameters and execute the pipeline
    
    """
    consumer: KafkaConsumer = KafkaConsumer(
          bootstrap_servers=['growing-krill-8066-eu1-kafka.upstash.io:9092' ],
  sasl_mechanism='SCRAM-SHA-256',
  security_protocol='SASL_SSL',
  sasl_plain_username= os.getenv("SASL_PLAIN_USERNAME"),
  sasl_plain_password=os.getenv("SASL_PLAIN_PASSWORD"),
        auto_offset_reset='earliest',
        consumer_timeout_ms=1000,
        topics=['']
    )
    message = consumer.poll(timeout_ms=60000)
    if message is not None:
        


@router.get("/requestJob/surface_reconstruction/bacalhau")
async def runpipeline_Bacalhau(request: Request, response: Response):
    """
    gets the input parameters from the cronjob()
    
    
    """
    
    while 


@router.get("/requestJob/surface_reconstruction/ECS")
async def runpipeline_ECS(request: Request, response: Response):
    '''
    It parses the input parameters from requests(consisting of the parameters of the compute job) from the kafka queue. 
    then pulls the docker image of reconstruction-pipline and executes it on the ECS which schedules it to the bacalhau node.
    )
    
    the input parameters are planned as follows
    coordX 
    coordY 
    username 
    ipfs_shp
    ipfs_pipeline
    shpFile 
    '''

    # dockerImg: str, params:InputParametersPoint
   
    try:
        body = await request.json()
        if "coordinate" not in body or "ipfs_shp" not in body:
            raise Exception("invalid parameters from bot/ message, need to pass parameters")
        
        params = []
        for param in body["params"]:
            params.append(param)
    except Exception as e:
       response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
       return {"message": str(e)}


    try:
        
        response = client.run_task(
        cluster= 'extralabs-dev',
        launchType='FARGATE',
        taskDefinition='reconstruction-pipeline',
        count=1,
        networkConfiguration={
          'awsvpcConfiguration': {
            'subnets': [
               os.enviorn['ECS_SUBNET'],
            ],
            'securityGroups': [
                os.environ['ECS_SEC_GROUP'],
            ],
            'assignPublicIp': 'ENABLED'
            }              
        }           
    )
        logging.debug(response)

    except SystemError as s:
        print(s)


@router.get("/state/{job_id}")
def get_state(clientID: str, response: Response):
    """
    fetches the status current  jobs listed by the user on our network
    clientId: is the generated clientId of the user (generated after running the user profile).
    """
    try:
        resultingJobs = states(clientID)
        return resultingJobs
    except SystemError as s:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": str(e)}


@router.get("/job/{job_id}")
def getJobResults(jobId: str, response: Response):
    """
    fetches the result of the jobs that are executed for the given client and stored in ipfs.
    this will be called by the trigger bot periodically to get the results.
    clientId: is the user identifier.
    jobId: is the job identifier.
    """

    try:
        result = results(job_id=jobId)
        return result       
    except Exception as h:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": str(h)}


scheduler.scheduled_job('cron', interval=60, func=cron_job)