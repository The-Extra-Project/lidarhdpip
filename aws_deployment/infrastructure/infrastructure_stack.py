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
class DiscordBotDeployment(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope,construct_id, **kwargs)
        ## then hosting the corresponding script for lambda consumer         
        bots = _lambda.Function(
            self, "DiscordBot", 
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="circombot.init_fn",
            code= _lambda.Code.from_asset(path=os.path.abspath(''))
        )
        
        
        bots.add_to_role_policy(
            statement= iam.PolicyStatement(
            actions=["connect:StartTls"],
            resources=["arn:aws:execute-api:*:*:*/*/*/*"],
            conditions={"StringLike": {"aws:SourceArn": "arn:aws:iam::*:root:*"}}
            )
        )
      