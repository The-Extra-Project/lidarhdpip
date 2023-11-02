"""
this script defines éthe command functions that it runs from the georender package
"""

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context 
import platform
import random
import aiohttp
import time

from bots.consumer.kafkaConsumer import kafka_consume_message_jobResult
from bots.producer.kafkaProducer import kafka_producer_job_cropPoint, kafka_producer_polygon


class UserCommands(commands.Cog, name= "lidarhd" ):
    imageName: str
    client: str
    
    
    def __init__(self,bot):
        self.bot = bot
        self.response = discord.embeds.Embed(
            title="lidarHD bot service",
            description="generated result of bacalhau job")
        
   
    async def on_ready(self):
        print(f'added as the {self.user}!')
    
    
    ## job for cropping operations       
    @commands.command(name="job_point", describes="creates user jobs on the given coordinates")
    async def job_point(self, context:Context, Xcoord, YCoord,ipfs_shp_file, ipfs_template_file):
        """
        fetches the input from the user and transfers to the output. 
        """
        username = context.author.name
        print(f'Message transferred to the bacalhau compute job: {Xcoord, YCoord, username, ipfs_shp_file, ipfs_template_file }')
        try:
            kafka_producer_job_cropPoint(Xcoord=Xcoord, Ycoord=YCoord, username=username, ipfs_shp_file=ipfs_shp_file, ipfs_filename_template=ipfs_template_file)
        ## check whether there is any message in the 
            time.sleep(2)
            await context.send("waited for 10 sec(for test), checking if the consume message is generated")        
            await kafka_consume_message_jobResult(topic='bacalhau_job_compute', keyID=username)

        except Exception as e:
            print("exception in the job")
         
    
    @commands.command(name="job_polygon", describes="creates cropping job for generating the polygon job")     
    async def job_polygon(self, context:Context, X_longitude:str, X_lattitude:str, Y_longitude: str, Y_lattitude:str, ipfs_shp_file, ipfs_template_file ):    
        """
        generates the laz file result link after running the compute job.
        
        """
        username = context.author.name
        coordinates = [X_longitude, X_lattitude, Y_longitude, Y_lattitude, ipfs_shp_file, ipfs_template_file]
        
        try:
            kafka_producer_polygon(coordinates=coordinates, username=username, ipfs_shp_file=ipfs_shp_file, ipfs_filename_template=ipfs_template_file)            
            await context.send("the cropping job using polygon is created, wait for the result")
            # add the kafka consumer job that parses and gets the path for the user in order to fetch the result.
            self.response.add_field(name="result output:", value=100)
        except Exception as e:
            print( "exception" + e.with_traceback)
    


        
    @commands.command(name="get_status", describes="gets the output status of the compute job")
    @app_commands.describe(scope="defines the details about the current job status")
    async def get_status(self,context: Context, jobId: str, username):
        print("the status of the your previous job by {} of given jobId {} is follows:".format(context.author.name,jobId))
        
        kafka_consume_message_jobResult(topic='bacalhau_compute_job',keyID=username)




async def setup(bot):
    await bot.add_cog(UserCommands(bot))