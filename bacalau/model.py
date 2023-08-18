from pydantic import BaseModel
from typing import List
from enum import Enum
from typing import Union, List


"""
this script defines the python api response models and results.

"""
class JobStatus(Enum):
    submitted = 1
    rejected = 2
    completed = 3

class InputParametersPoint():
    coordX: str
    coordY: str
    username: str
    ipfs_image: str

class JobComputation(BaseModel):
    username: str
    coordX: str
    coordY: str
    
class JsonReturnFormat(BaseModel):
    json_format: Union[dict, str] 


class JobResults(BaseModel):
    resultingIds: List[str]

class ClientJobComputationMapping(BaseModel):
    client_id: str	
    job_id: str	
    job_status: JobComputation 	
    docker_image_name: str	
    