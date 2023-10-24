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
from consumer.kafkaConsumer import  kafka_consume_list_jobs
from producer.kafkaProducer import  kafka_produce_pipeline_reconstruction

class UserCommands(commands.Cog, name= "lidarhd" ):
    def __init__(self,bot):
        self.bot = bot
        
    async def on_ready(self):
        print(f'added as the {self.user}!')

    @commands.hybrid_command(name="status", describes="gets the output status of the compute job")
    async def get_status(self,context: Context):
        print("the status of the your previous job by {} of given jobID:".format(context.author.name))
        username = context.author.name
        time.sleep(10)
        kafka_consume_list_jobs(topic='bacalhau_result_job',keyID=username)


    @commands.hybrid_command(name="surfacereconstruction", description="takes the 3D point cloud in las format and generates the corresponding polygon representation of file in ply format")
    async def do_surface_reconstruction_pipeline_point(self, context: Context, Xcoord, YCoord,ipfs_shp_file, ipfs_template_file,  in_file: str, algorithm_category: int ):
        print(f'Message transferred to the bacalhau surface reconstruction job: {in_file, algorithm_category}')
        kafka_produce_pipeline_reconstruction(username=context.author.name, pathInputlasFile=in_file, Xcoord=Xcoord, YCoord=YCoord, ipfs_shp_file=ipfs_shp_file,ipfs_template_file=ipfs_template_file)


async def setup(bot):
    await bot.add_cog(UserCommands(bot))