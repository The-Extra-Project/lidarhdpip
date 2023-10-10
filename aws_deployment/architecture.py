from diagrams import Diagram, Cluster
from diagrams.saas.chat import Discord
from diagrams.aws.integration import  SQS
from diagrams.aws.compute import EC2, ECS, Lambda
from diagrams.aws.network import APIGateway

with Diagram("bot-architecture",show=True):
    frontend = [Discord("circumbot")]
    circumbot = Lambda("circumbot")
    kafkaoperations = [SQS("broker-command-producer"), SQS("broker-command-consumer")]
    consumer = Lambda("consuming requests(intervals)")
    pipeline = ECS("cluster")
    clusterAPI = APIGateway("bacalhau-cluster-api")
    
    frontend >> circumbot >> kafkaoperations[0] >> consumer
    with Cluster("hosted bacalhau instances"):
        frontend >> kafkaoperations[0]
        kafkaoperations[0] >> kafkaoperations[1]
        kafkaoperations[1] >> clusterAPI >> pipeline
        consumer >> EC2("requester node")  
        EC2("requester node") >> [ECS("spawning bacalhau instance (based on job)")]