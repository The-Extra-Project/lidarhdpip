# import aws_cdk as cdk
# from constructs import Construct
# from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep


# class lidarHdStack(cdk.Stack):
#     def __init__(self, scope: Construct, construct_id: str, **kwargs)-> None :
#         super().__init__(scope, construct_id, **kwargs)
#         pipeline =  CodePipeline(self, "Pipeline",
#                         pipeline_name="MyPipeline",
#                         synth=ShellStep("Synth",
#                             input=CodePipelineSource.git_hub("The-Extra-Project/lidarhdpip", "dev-adding-v0.1"),
#                             commands=["npm install -g aws-cdk",
#                                 "curl -sSL https://install.python-poetry.org | python3 -",
#                                 "poetry update",
#                                 "cdk synth"]
#                         )
#                     )