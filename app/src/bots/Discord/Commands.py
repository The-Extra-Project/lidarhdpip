"""
this script defines the command functions that it runs from the georender package
"""

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context, Bot 
import platform
import random
import aiohttp

#from src.bots.Discord.kafkaMessages import kafka_producer_message


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
    
    
    @commands.command(name="on_message", describes="allows user to create an job for computing las for the given area defined by geo-coordianaates")
    @app_commands.describe(scope="inputs are X and Y coordinates for the area you want to find 3D scans")
    async def on_message(self, context:Context, Xcoord, YCoord):
        """
        fetches the input from the user and transfers to the output 
        
        """
        username = context.author.name
        print(f'Message transferred to the bacalhau compute job: {Xcoord, YCoord, username}')
        #kafka_producer_message(Xcoord=Xcoord, Ycoord=YCoord, username=username)

    @commands.command(name="getting status", describes="gets the output status of the compute job")
    @app_commands.describe(scope="defines the details about the current job status")
    async def get_status(self,context: Context, jobId: str):
        print("the status of the your previous job by {} of given jobId {} is follows:".format(context.author.name,jobId))

async def setup(bot):
    await bot.add_cog(UserCommands(bot))