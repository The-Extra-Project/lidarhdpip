"""
bacalau script that deploys the georender dockerised container on the bacalau.
this will be called by the kafka topic once there is compute bandwidth available.
"""
import json
from utils.model_helper import JobResults, InputParametersPoint
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
import pprint
import http

load_dotenv(dotenv_path='.env')
config = dotenv_values(dotenv_path='.env')

surface_reconstruction = 'devextralabs/bacalhau_surface_reconstruction'

def createJobBacalauPoint(parameter: InputParametersPoint) -> any:
    '''
    pulls the docker image of georender and executes it on the bacalau compute network
    for example, in the case of the georender, it will be as follows:
    params[0]: is the X coordinate of the geometric coordinates
    params[1]: is the Y coordinate of the geometric coordinates
    params[2]: username of the discord that wants to execute the job
    params[3]:  cid link for the shp file. 
    params[4]   cid link of pipeline template.
    params[5]: filename of the shp file that you want to render.
    params[6]: name of the docker image. 
    '''

    # dockerImg: str, params:InputParametersPoint
    
    coordX = parameter.coordX
    coordY = parameter.coordY
    username = parameter.username
    ipfs_shp_details = parameter.ipfs_image
    ipfs_pipeline_details = parameter.ipfs_pipeline
    shpFile = parameter.filename_shp
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
            entrypoint=[coordX, coordY, username, ipfs_shp_details,ipfs_pipeline_details, shpFile]
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
    


def execute_reconstruction_pipeline(
    Xcoord="43.2946",
    Ycoord="5.3695",
    username="test",
    ipfs_shp_file="bafkreicxd6u4avrcytevtvehaaimqbsqe5qerohji2nikcbfrh6ccb3lgu",
    filename="pipeline_template.json",
    algorithm_surface_reconstruction="0", #(poisson)
                ):
    """
    function to call the hosted pipeline construction container on ECS which will in turn run the intermediate series of computations on the bacalhau
    """
    
    pass
    



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
        resultData = results(clientId)
        vectorize_outputs(resultData)
    except Exception as h:
        print(h)

def vectorize_outputs(data:dict):
    """
    gets the succinct output results from the json file.
    
    Parameters
    -----------
    jsonOutput is the json format resultinng from the results api function. 
    
    Returns the formatted response from 
    
    """
    """
    {'results': [{'data': {'cid': 'QmYEqqNDdDrsRhPRShKHzsnZwBq3F59Ti3kQmv9En4i5Sw',
                       'metadata': None,
                       'name': 'job-710a0bc2-81d1-4025-8f80-5327ca3ce170-shard-0-host-QmYgxZiySj3MRkwLSL4X2MF5F9f2PMhAE3LV49XkfNL1o3',
                       'path': None,
                       'source_path': None,
                       'storage_source': 'IPFS',
                       'url': None},
              'node_id': 'QmYgxZiySj3MRkwLSL4X2MF5F9f2PMhAE3LV49XkfNL1o3',
              'shard_index': None}]
              
              }
    """
    vectorized_result = {}
    results = data["results"]

    for params in results:
        param_dict = params["data"]
        vectorized_result[param_dict["name"]] = {
        "cid": results["cid"],
        "metadata": results["metadata"],
        "path": results["path"],
        "source_path": results["source_path"],
        "storage_source": results["storage_source"],
        "url": results["url"],  
        "node_id": params["node_id"]
        }
    
    
    pprint.pprint(vectorized_result,indent=4)   



# def create_surface_reconstructionJob(paramsReconstrcution:any): 
    
#     input_las = paramsReconstruction.in_file
#     algorithm_file = paramsReconstruction.algo
    



    




if __name__ == "__main__":
    inputParams: InputParametersPoint = InputParametersPoint
    if (test == True):
    ## passing the parameters via the cli params (for testing)
        [inputParams.coordX , inputParams.coordY, inputParams.username, inputParams.ipfs_image, inputParams.dockerimage] = sys.argv[1:6]
        print( ''+"parameters finalized: {},{},{},{},{} ".format(inputParams.coordX , inputParams.coordY, inputParams.username, inputParams.ipfs_image, inputParams.dockerimage))
        createJobBacalauPoint(inputParams)