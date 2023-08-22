#!/usr/bin/env python3
import os

import aws_cdk as cdk

from infrastructure.infrastructure_stack import InfrastructureStack
#from infrastructure.ci_pipeline import lidarHdStack

app = cdk.App()

InfrastructureStack(app,construct_id="InfrastructureStack")

app.synth()
