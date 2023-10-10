from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_apigatewayv2 as api,
    aws_ecs as ecs,
)

import os
from constructs import Construct

"""
Credits to [aws-cdk examples](https://github.com/aws-samples/aws-cdk-examples) for the reference examples. 
"""
class InfrastructureStack(Stack):
    job_scheduler: _lambda.DockerImageFunction
    bots: _lambda.DockerImageFunction
    visualization: _lambda.DockerImageFunction
    role: iam.Role

    def __init__(self, scope: Construct, construct_id: str, cluster_name: str ,**kwargs ) -> None:
        super().__init__(scope,construct_id, **kwargs)
        ## then hosting the corresponding script for lambda consumer
        self.define_lambda_service()
        self.define_role_access()
        self.connect_to_cluster(cluster_name)
      
      
      
    def connect_to_cluster(self,cluster_name: ecs.Cluster):
        
        if cluster_name:
            ## connecting to the pre-existing cluster.
            self.ecs = ecs.Cluster.from_cluster()
        
      
    
    def define_lambda_service(self):  
        self.job_scheduler = _lambda.DockerImageFunction(
            self, "job_scheduler", 
            architecture=_lambda.Architecture.ARM_64,
            code= _lambda.DockerImageCode.from_image_asset(directory= os.path.abspath('../job_scheduler'))
        )      

        self.bots = _lambda.DockerImageFunction(
            self, "bots", 
            architecture=_lambda.Architecture.ARM_64,
            code= _lambda.DockerImageCode.from_image_asset(directory=os.path.abspath('../bots/'))
        )
        
        self.visualization = _lambda.DockerImageFunction(
            self, "vizualization",
            architecture=_lambda.Architecture.ARM_64,
            code= _lambda.DockerImageCode.from_image_asset(directory=os.path.abspath('../visualization/'))
        )
        
    def define_role_access(self):
        self.role = iam.Role(self,"discord", assumed_by=iam.ServicePrincipal("sns.amazonaws.com"))         
        discord_access_policy = iam.PolicyStatement(actions=["lambda:InvokeFunction"], resources=[self.bots.function_arn])
        bots_access_policy = iam.PolicyStatement(actions=["lambda:InvokeFunction"], resources=[self.job_scheduler.function_arn])
        visualization_access_policy = iam.PolicyStatement(actions=["lambda:InvokeFunction"], resources=[self.visualization.function_arn])
        self.role.add_to_policy(discord_access_policy)
        self.role.add_to_policy(bots_access_policy) 
        self.role.add_to_policy(visualization_access_policy) 