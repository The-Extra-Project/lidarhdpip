import pytest
import requests
from fastapi.testclient import TestClient
from fastapi import Request
import sys

from route.bacalau_script import router
from pydantic import BaseModel 

client = TestClient(router)

class Request(BaseModel):
    xcoord: str
    ycoord: str
    ipfs_shp:str
    template_name: str
    reconstruction_flag: int


def create_task():
    
    parameters : Request = {
        "xcoord": '34',
        "ycoord": "22",
        "ipfs_shp": "QmW3714d18125599581345",
        "template_name":"pipeline_template",
        "reconstruction_flag": '0'
    }
    
    response = client.get("/jobs/requestJob", params=parameters)
    
    assert response.status_code == 200
    
    