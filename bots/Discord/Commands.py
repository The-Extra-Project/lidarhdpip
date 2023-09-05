"""
this script defines the command functions that it runs from the georender package
"""

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context 
import platform
import random
import aiohttp
import time

from consumer.kafkaConsumer import kafka_consume_message_jobResult, kafka_consume_list_jobs
from producer.kafkaProducer import kafka_producer_job


class UserCommands(commands.Cog, name= "lidarhd" ):
    def __init__(self,bot):
        self.bot = bot
        
    # def __init__(self, dockerimageId, clientId: str, bot) -> None:
    #     self.imageName = dockerimageId
    #     self.client = clientId # corresponds to the user id that want to access the infrastructure.
    #     self.bot = bot
   
    async def on_ready(self):
        print(f'added as the {self.user}!')
    
    
    @commands.hybrid_command(name="job_point", describes="creates user jobs on the given coordinates")
    @app_commands.describe(scope="inputs are X and Y coordinates for the area you want to find 3D scans")
    async def job_point(self, context:Context, Xcoord, YCoord,ipfs_shp_file, ipfs_template_file):
        """
        fetches the input from the user and transfers to the output. 
        """
        username = context.author.name
        print(f'Message transferred to the bacalhau compute job: {Xcoord, YCoord, ipfs_shp_file, ipfs_template_file }')
        kafka_producer_job(Xcoord=Xcoord, Ycoord=YCoord, username=username, ipfs_shp_file=ipfs_shp_file, ipfs_filename_template=ipfs_template_file)
        ## check whether there is any message in the 
        time.sleep(10)
        username = context.author.name
        print("waited for 10 sec(for test), checking if the consume message is generated")        
        kafka_consume_message_jobResult(topic='bacalhau_result_job', keyID=username)
        print("command is generated")


    @commands.hybrid_command(name="get_status", describes="gets the output status of the compute job")
    @app_commands.describe(scope="defines the details about the current job status")
    async def get_status(self,context: Context, jobId: str):
        print("the status of the your previous job by {} of given jobId {} is follows:".format(context.author.name,jobId))
        username = context.author.name
        time.sleep(10)
        kafka_consume_list_jobs(topic='bacalhau_result_job',keyID=username)


    @commands.hybrid_command(name="ger_jobIds", describes="gets the  status of the jobIds that are currently listed for the user")
    @app_commands.describe(scope="defines the details about the current job status")
    async def get_jobIds(self, context:Context, ):
        print("the status of the your  all previous job by {}=>".format(context.author.name))
        time.sleep(10)
        username = context.author.name
        kafka_consume_list_jobs(topic='bacalhau_result_job')
        
        




async def setup(bot):
    await bot.add_cog(UserCommands(bot))