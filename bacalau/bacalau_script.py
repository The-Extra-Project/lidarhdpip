import requests
from typing import Union, List
import json
from model import JobComputation, JobResults, JsonReturnFormat, InputParametersPoint
"""
bacalau script that deploys the georender dockerised container on the bacalau.
this will be called by the kafka topic once there is compute bandwidth available.
"""

from bacalhau_apiclient.models.deal import Deal
from bacalhau_apiclient.models.job_spec_docker import JobSpecDocker
from bacalhau_apiclient.models.job_spec_language import JobSpecLanguage
from bacalhau_apiclient.models.publisher_spec import PublisherSpec
from bacalhau_apiclient.models.spec import Spec
from bacalhau_apiclient.models.storage_spec import StorageSpec
from bacalhau_sdk.api import submit
from bacalhau_sdk.config import get_client_id
from bacalhau_sdk.api import results, states

from dotenv import load_dotenv, dotenv_values

load_dotenv(dotenv_path='./.env')

config = dotenv_values(dotenv_path='.env')
from kafka import KafkaProducer, KafkaConsumer

bacalhauProducer = KafkaProducer(
  bootstrap_servers=[config["KAFKA_BROKER_URL"]],
  sasl_mechanism='SCRAM-SHA-256',
  security_protocol='SASL_SSL',
  sasl_plain_username=config["SASL_PLAIN_USERNAME"],
  sasl_plain_password=config["SASL_PLAIN_PASSWORD"],
)

bacalhauConsumer = KafkaConsumer(
          bootstrap_servers=[config["KAFKA_BROKER_URL"]],
  sasl_mechanism='SCRAM-SHA-256',
  security_protocol='SASL_SSL',
  sasl_plain_username=config["SASL_PLAIN_USERNAME"],
  sasl_plain_password=config["SASL_PLAIN_PASSWORD"],
        auto_offset_reset='earliest',
        consumer_timeout_ms=1000
    )


def createJobBacalauPoint() -> JsonReturnFormat:
    '''
    pulls the docker image of georender and executes it on the bacalau compute network
    for example, in the case of the georender, it will be as follows:
    params[0]: is the X coordinate of the geometric coordinates
    params[1]: is the Y coordinate of the geometric coordinates
    dockerImg: name of the registry file that is hosted in the dockerhub
    '''

    # dockerImg: str, params:InputParametersPoint
    dockerImg: str
    params: InputParametersPoint
    ## TODO: fetch the different channel name using the settings defined like in src/stashed_config
    bacalhauConsumer.subscribe(['bacalhau_compute_job'])
    
    ## only consume the first message from the given 
    
    parameter = bacalhauConsumer.poll(timeout=1)
    if parameter:
        print("parameter retrieved" + parameter)
    
    [coordX, coordY, username, ipfs_details] = parameter.value.decode('utf-8').split(',')
    

    InputJob = dict(
        APIBeta= 'v0.1',
            ClientID=get_client_id(),
    Spec=Spec(
        engine="Docker",
        verifier="Noop",
        publisher_spec= PublisherSpec("ipfs"),
        docker=JobSpecDocker(
            image=dockerImg,
            entrypoint=[coordX, coordY, username, ipfs_details]
        ),
        language=JobSpecLanguage(job_context=None),
        wasm=None,
        resources=None,
        timeout=1800,
        outputs=[
            StorageSpec(
                storage_source="IPFS",
                name="outputs",
                path="/outputs",
            )
        ],
        deal=Deal(concurrency=1, confidence=0, min_bids=0),
        do_not_track=False,
    ),
    )

    try:
        job_json_details = json.loads(submit(InputJob))
        print(job_json_details)
            #jobresults = JobComputation(job)

        return job_json_details
    except SystemError as s:
        print(s)
    
def listJobs(clientId: str) -> JobResults:
    """
    fetches the status current status of listed jobs in the network
    clientId: is the generated clientId of the user.
    """
    try:
        resultingJobs = JobResults(states(get_client_id()))
        return resultingJobs
    except SystemError as s:
        print(s)


def getJobResults(clientId: str, jobId: str):
    """
    fetches the result of the jobs that are executed for the given client and stored in ipfs.
    this will be called by the trigger bot periodically to get the results.
    clientId: is the user identifier.
    jobId: is the job identifier.
    """

    try:
       return results(clientId)

    except HTTPException as h:
        print(h)





