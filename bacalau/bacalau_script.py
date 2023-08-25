"""
bacalau script that deploys the georender dockerised container on the bacalau.
this will be called by the kafka topic once there is compute bandwidth available.
"""

import json
from model import JobResults, JsonReturnFormat, InputParametersPoint
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
import sys

load_dotenv(dotenv_path='./.env')
config = dotenv_values(dotenv_path='.env')


def createJobBacalauPoint(parameter: InputParametersPoint) -> any:
    '''
    pulls the docker image of georender and executes it on the bacalau compute network
    for example, in the case of the georender, it will be as follows:
    params[0]: is the X coordinate of the geometric coordinates
    params[1]: is the Y coordinate of the geometric coordinates
    params[2]: username of the discord that wants to execute the job
    params[3]: ipfsImage is the cid link for the shp and other mapping files stored from https://pcrs.ign.fr/version3
    params[4]: name of the docker image 
    '''

    # dockerImg: str, params:InputParametersPoint
    
    coordX:str = parameter.coordX
    coordY = parameter.coordY
    username = parameter.username
    ipfs_details = parameter.ipfs_image
    dockerImg = parameter.dockerimage
  
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
    
def listJobs() -> JobResults:
    """
    fetches the status current status of listed jobs in the network
    clientId: is the generated clientId of the user.
    """
    try:
        resultingJobs = JobResults(states(get_client_id()))
        return resultingJobs
    except SystemError as s:
        print(s)

def getJobResults(clientId: str):
    """
    fetches the result of the jobs that are executed for the given client and stored in ipfs.
    this will be called by the trigger bot periodically to get the results.
    clientId: is the user identifier.
    jobId: is the job identifier.
    """

    try:
       return results(clientId)

    except Exception as h:
        print(h)

test = True

if __name__ == "__main__":
    inputParams: InputParametersPoint = InputParametersPoint
    if (test == True):
    ## passing the parameters via the cli params (for testing)
        [inputParams.coordX , inputParams.coordY, inputParams.username, inputParams.ipfs_image, inputParams.dockerimage] = sys.argv[1:6]
        print( ''+"parameters finalized: {},{},{},{},{} ".format(inputParams.coordX , inputParams.coordY, inputParams.username, inputParams.ipfs_image, inputParams.dockerimage))
        createJobBacalauPoint(inputParams)