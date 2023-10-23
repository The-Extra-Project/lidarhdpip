import pytest
import requests
from fastapi.testclient import TestClient
from fastapi import Request
import sys

from job_scheduler.route.bacalau_script import router
from pydantic import BaseModel 

client = TestClient(router)

class RequestJobPointReconstruction(BaseModel):
    xcoord: str
    ycoord: str
    ipfs_shp:str
    template_name: str
    reconstruction_flag: int

class RequestCityGMLReconstruction(BaseModel):
    yamlFile: str
    openJSON_destination_directory: str

    
    
    
def create_job_task():
    
    parameters : Request = {
        "xcoord": '34',
        "ycoord": "22",
        "ipfs_shp": "QmW3714d18125599581345",
        "template_name":"pipeline_template",
        "reconstruction_flag": '0'
    }
    
    response = client.get("/jobs/requestJob/surface_reconstruction/ECS", params=parameters)
    
    assert response.status_code == 200
    
def get_values():
    pass