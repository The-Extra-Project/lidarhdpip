import pytest
from bacalau_script import createJobBacalau, listJobs, getJobResults, app
from model import JobComputation, JobResults
from fastapi.testclient import TestClient


test = TestClient(app)

def test_job_computation():
    x_param = "10.123"
    y_param = "30.456"

    dockerImgFile = "lxet/lidar_geocoordinate"


    response_job = test.get("/compute/createJob", params= {
        "params": [x_param, y_param], "dockerImgFile": dockerImgFile
    })

    #job = createJobBacalau([x_param, y_param], dockerImgFile)

    assert response_job.status_code  == 200
    assert response_job["job"]["metadata"]["id"] is not None
    
