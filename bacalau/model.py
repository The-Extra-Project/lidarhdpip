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
    ipfs_pipeline: str
    filename_shp:str
    dockerimage: str

class InputParametersCityGML():
    yamlFile: str
    ObjFile: str
    gmlOutputFile: str


    
class JsonReturnFormat(BaseModel):
    json_format: Union[dict, str] 


class JobResults(BaseModel):
    resultingIds: List[str]
    