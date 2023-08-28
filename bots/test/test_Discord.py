import pytest
from  Discord.circombot import on_ready, on_message, on_command_completion, on_command_error, bot
import asyncio
import discord.ext.test as dpytest


def test_initialization():
    dpytest.configure(bot)
    
    