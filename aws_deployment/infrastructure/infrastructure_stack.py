from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_apigatewayv2 as api,
)

import os
from constructs import Construct
"""

Credits to [aws-cdk examples](https://github.com/aws-samples/aws-cdk-examples) for the reference examples. 

"""
class InfrastructureStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope,construct_id, **kwargs)
        ## then hosting the corresponding script for lambda consumer
        
        bacalhau = _lambda.DockerImageFunction(
            self, "bacalau", 
            architecture=_lambda.Architecture.ARM_64,
            code= _lambda.DockerImageCode.from_image_asset(directory= os.path.abspath('../bacalau'))
        )      
        bots = _lambda.DockerImageFunction(
            self, "bots", 
            
            architecture=_lambda.Architecture.ARM_64,
            code= _lambda.DockerImageCode.from_image_asset(directory=os.path.abspath('../bots/'))
        )
        
        visualization = _lambda.DockerImageFunction(
            self, "vizualization",
            architecture=_lambda.Architecture.ARM_64,
            code= _lambda.DockerImageCode.from_image_asset(directory=os.path.abspath('../visualization/'))
        )
        
        role = iam.Role(self,"discord", assumed_by=iam.ServicePrincipal("sns.amazonaws.com") ) 
        
        discord_access_policy = iam.PolicyStatement(actions=["lambda:InvokeFunction"], resources=[bots.function_arn])
        bots_access_policy = iam.PolicyStatement(actions=["lambda:InvokeFunction"], resources=[bacalhau.function_arn])
        visualization_access_policy = iam.PolicyStatement(actions=["lambda:InvokeFunction"], resources=[visualization.function_arn])
        
        role.add_to_policy(discord_access_policy)
        role.add_to_policy(bots_access_policy) 
        role.add_to_policy(visualization_access_policy) 