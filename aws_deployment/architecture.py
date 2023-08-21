from diagrams import Diagram, Cluster
from diagrams.saas.chat import Discord, Telegram
from diagrams.aws.integration import  SQS
from diagrams.aws.compute import EC2, ECS, Lambda
from diagrams.aws.network import APIGateway

with Diagram("circum bot architecture", show=True):
    frontend = [Discord("circumbot")]
    circumbot = Lambda("circumbot")
    kafkaoperations = [SQS("broker-command-producer"), SQS("broker-command-consumer")]
    consumer = Lambda("consuming requests(intervals)")
    bacalhau_requesterNode = EC2("requester-node")
    clusterAPI = APIGateway("bacalhau-cluster-api")
    
    frontend >> circumbot >> kafkaoperations[0] >> consumer
    with Cluster("hosted bacalhau instances"):
        consumer >> EC2("requester node") 
        EC2("requester node") >> [ECS("spawning bacalhau instance (based on job)")]