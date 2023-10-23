import asyncio
import json
import os
import platform
import random
import sys
import logging
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context

sys.path.append('../../')
from bots.Discord.loggingFormatter import LoggingFormatter
from bots.consumer import kafkaConsumer
from  bots.producer import kafkaProducer
from  bots.Discord.Commands import setup

try:
    with open(f"{os.path.realpath(os.path.dirname(__file__))}/config.json") as file:
        config = json.load(file)
except FileNotFoundError as notFound:
    print(notFound)
    
intents = discord.Intents.default()
intents.message_content = True

bot: Bot = Bot(
command_prefix= "/",
intents=intents,
help_command=None,
)

## taken from krypt0nn repo that renders the logs them in the prettify way:
logger = logging.getLogger("discord.log")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())

# File handler
file_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
)


file_handler.setFormatter(file_handler_formatter)

# Add the handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)
bot.logger = logger


@bot.event
async def on_ready() -> None:
    """
    The code in this event is executed when the bot is ready.
    """
    bot.logger.info(f"Logged in globally as {bot.user.name}")
    bot.logger.info(f"discord.py API version: {discord.__version__}")
    bot.logger.info(f"Python version: {platform.python_version()}")
    bot.logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    bot.logger.info("-------------------")
    
    if config["sync_commands_globally"]:
        bot.logger.info("Syncing commands globally...")
        await bot.tree.sync()
        bot.logger.info("commands synced, go now to the discord channel in order to start running commands")



@tasks.loop(minutes=1.0)
async def sending_results_job(ctx:Context):
    bot.logger.info("Checking for new job results...")
    result = kafkaConsumer.kafka_consume_message_jobInput(topic='bacalhau_job_compute', keyID=ctx.author.id)
    ctx.reply("hi {}, the compute is scheduled and the progress is {}".format(ctx.author,ctx.args))
    


@bot.event
async def on_message(message: discord.Message) -> None:
    """
    The code in this event is executed every time someone sends a message, with or without the prefix

    :param message: The message that was sent.
    """
    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)
    message.reply("hiya, your job will be scheduled in a min")    
    

@bot.event
async def on_command_completion(context: Context) -> None:
    """
    The code in this event is executed every time a normal command has been *successfully* executed.

    :param context: The context of the command that has been executed.
    """
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    if context.guild is not None:
        bot.logger.info(
            f"Executed {executed_command}  by {context.author} + '&' +(ID: {context.author.id})"
        )
    else:
        bot.logger.info(
            f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs"
        )


@bot.event
async def on_command_error(context: Context, error) -> None:
    """
    The code in this event is executed every time a normal valid command catches an error.

    :param context: The context of the normal command that failed executing.
    :param error: The error that has been faced.
    """
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            description=f"**Please slow down** - You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0xE02B2B,
        )
        await context.send(embed=embed)
 
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error!",
            # We need to capitalize because the command arguments have no capital letter in the code.
            description=str(error).capitalize(),
            color=0xE02B2B,
        )
        await context.send(embed=embed)
    else:
        raise error


async def load_cogs(bot) -> None:
    try:
        await bot.load_extension(f"Commands")
        
        await setup(bot=bot)
        bot.logger.info("commands package loaded")
    except Exception as e:
        bot.logger.error(f"Failed to load extension from commands.py")
        
asyncio.run(load_cogs(bot=bot))
bot.run(config["token"])


