import dpytest
from  bots.Discord.circombot import  bot
from  bots.Discord.Commands import job_point, get_status
import asyncio
import discord.ext.test as dpytest

def test_initialization():
    dpytest.configure(bot)
    
    
# def test_command_create_job():
#      dpytest.message("job_point",)
    
    