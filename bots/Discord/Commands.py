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

from consumer.kafkaConsumer import kafka_consume_message_jobResult
from producer.kafkaProducer import kafka_producer_job


class UserCommands(commands.Cog, name= "lidarhd" ):
    imageName: str
    client: str
    
    
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
        print(f'Message transferred to the bacalhau compute job: {Xcoord, YCoord, username, ipfs_shp_file, ipfs_template_file }')
        kafka_producer_job(Xcoord=Xcoord, Ycoord=YCoord, username=username, ipfs_shp_file=ipfs_shp_file, ipfs_filename_template=ipfs_template_file)
        ## check whether there is any message in the 
        time.sleep(10)
        print("waited for 100 sec(for test), checking if the consume message is generated")        
        kafka_consume_message_jobResult(topic='bacalhau_job_compute', keyID=username)
        
    @commands.hybrid_command(name="get_status", describes="gets the output status of the compute job")
    @app_commands.describe(scope="defines the details about the current job status")
    async def get_status(self,context: Context, jobId: str, username):
        print("the status of the your previous job by {} of given jobId {} is follows:".format(context.author.name,jobId))
        
        #kafka_consume_message_jobResult(topic='bacalhau_compute_job',keyID=username)

async def setup(bot):
    await bot.add_cog(UserCommands(bot))