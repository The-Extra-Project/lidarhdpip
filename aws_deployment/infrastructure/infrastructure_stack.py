from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_sam as SAM,
    aws_apigatewayv2 as api,
    App
)

import os
from constructs import Construct

"""
credits to [aws-cdk examples](https://github.com/aws-samples/aws-cdk-examples) for the reference examples 

"""

class InfrastructureStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        circumbot = _lambda.Function(
            self,id="circumbot", handler="on_ready", runtime=_lambda.Runtime.PYTHON_3_11,
            code=_lambda.Code.from_asset(os.path.join(os.getcwd(), '../app/src/bots/Discord/'))
        )

        ## then hosting the corresponding script for lambda consumer
        
        producer = _lambda.Function(
            self, id="producer", handler="", runtime=_lambda.Runtime.PYTHON_3_11,
            code= _lambda.Code.from_asset(os.path.join(os.getcwd(), '../app/src/bots/producer')
        ))         
        consumer_bacalhau = _lambda.Function(
            self, id="consumer", handler="", runtime=_lambda.Runtime.PYTHON_3_11,
            code= _lambda.Code.from_asset(os.path.join(os.getcwd(), '../app/src/bots/consumer')
        ))
        
        bacalhau_script = _lambda.Function(
            self, id="bacalhau_script", runtime=_lambda.Runtime.PYTHON_3_11, handler="",
            code= _lambda.Code.from_asset(os.path.join(os.getcwd(), '../bacalau/'))
                                        )
        
        # vpc = ec2.Vpc(
        #     self,"bacalhau-deployment",
        #     nat_gateways=0,
        #     subnet_configuration=[ec2.SubnetConfiguration(name="public-permissioned-access",subnet_type=ec2.SubnetType.PUBLIC)]
        # )
        
        role = iam.Role(self,"discord", assumed_by=iam.ServicePrincipal("sns.amazonaws.com") ) 
        discord_access_policy = iam.PolicyStatement(actions=["lambda:InvokeFunction"], resources=[circumbot.function_arn])
        producer_access_policy = iam.PolicyStatement(actions=["lambda:InvokeFunction"], resources=[producer.function_arn])
        consumer_access_policy = iam.PolicyStatement(actions=["lambda:InvokeFunction"], resources=[consumer_bacalhau.function_arn])
        
        role.add_to_policy(discord_access_policy)
        role.add_to_policy(producer_access_policy) 
        role.add_to_policy(consumer_access_policy) 
        
