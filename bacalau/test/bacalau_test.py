import pytest
from model import InputParametersPoint
from bacalau.test.mock.bot import kafka_producer_mock_job_message
from bacalau_script import createJobBacalauPoint, listJobs, getJobResults, app
from model import JobComputation, JobResults
from bacalau.broker.bacalhauConsumer import *
from bacalau.broker.bacalhauProducer import *


testParams = InputParametersPoint()
testParams.coordX = "34"
testParams.coordY = "42"
testParams.username = "test"
testParams.ipfs_image = ""
testParams.ipfs_pipeline = ""
testParams.dockerimage = "devextralabs/georender"
    
params = InputParametersPoint(testParams.coordX, testParams.coordY, testParams.username, testParams.ipfs_image, testParams.ipfs_pipeline,testParams.dockerimage)
    
def test_job_computation():
    assert createJobBacalauPoint(parameter=params) is not None
    
def test_list_jobs():
    assert listJobs() is not None



def test_get_result():
    try:
        assert test_get_result() is not None
    except Exception as e:
        print(e)
        
##now testing the kafka messaging stream
def test_kafka_submit_job():

    kafka_producer_mock_job_message()
    time.sleep(4)
    kafka_consume_message_jobCommand_point()
    assert consumer.end_offsets() is  None
    
def test_kafka_generate_result():
    offset_id = consumer.position('bacalhau-compute-job')
    kafka_producer_Job_result()
    time.sleep(4)
    kafka_consume_result_status("test")
    
    