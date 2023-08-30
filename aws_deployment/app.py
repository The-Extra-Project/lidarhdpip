#!/usr/bin/env python3
import os

import aws_cdk as cdk
import argparse
from infrastructure.infrastructure_stack import InfrastructureStack
import sys
#from infrastructure.ci_pipeline import lidarHdStack

app = cdk.App()
## give specific name to your stack and then use python app.py.
InfrastructureStack(app,construct_id="")
app.synth()
