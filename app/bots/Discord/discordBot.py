import discord
from discord.ext.commands import Bot, Context
from discord.ext import commands, tasks
from dotenv import load_dotenv, dotenv_values
import logging
import platform
from kafka import KafkaProducer, KafkaConsumer
import os
import random
import asyncio


load_dotenv(dotenv_path='../../.env')

config = dotenv_values(dotenv_path='../../.env')

intents = discord.Intents.default()
logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)


bot = Bot(
command_prefix= commands.when_mentioned_or(),
intents=intents,
help_command=None,
)

global producer
global consumer
producer = KafkaProducer(
  bootstrap_servers=[config["KAFKA_BROKER_URL"]],
  sasl_mechanism='SCRAM-SHA-256',
  security_protocol='SASL_SSL',
  sasl_plain_username=config["SASL_PLAIN_USERNAME"],
  sasl_plain_password=config["SASL_PLAIN_PASSWORD"],
)

consumer = KafkaConsumer(
          bootstrap_servers=[config["KAFKA_BROKER_URL"]],
  sasl_mechanism='SCRAM-SHA-256',
  security_protocol='SASL_SSL',
  sasl_plain_username=config["SASL_PLAIN_USERNAME"],
  sasl_plain_password=config["SASL_PLAIN_PASSWORD"],
        auto_offset_reset='earliest',
        consumer_timeout_ms=1000
    )
    



## kafka compute operations: 
def kafka_producer_message(Xcoord: str, Ycoord: str):
    """
    transfers the message entered by the user from the discord input to the kafka broker queue destined for bacalhau computation.
    message: the coordinates of the possition that the georender compute application will take as the parameter.
    """    
    
    
    result = producer.send(
        topic="bacalhau_compute_job",
        value=(Xcoord + ',' + Ycoord).encode('utf-8'),
        )
    print("Sending msg \"{},{}\"".format(Xcoord, Ycoord))
    print(result)
    return True

    
def kafka_consumer():
    """
    This function will fetch the messages from the broker queue that are essentially the results from the bacalhau node, 
    read the message and then prints the result.
    
    TODO: this fn will be shifted to the georender along w/ allowing threading process """
    
    consumer.subscribe(['bacalhau_compute_job'])
    
    for msg in consumer:
        print(msg)
    producer.flush()
    producer.close()
    consumer.close()

@bot.event
async def on_ready() -> None:
    """
    The code in this event is executed when the bot is ready.
    """
    bot.logger.info(f"Logged in as {bot.user.name}")
    bot.logger.info(f"discord.py API version: {discord.__version__}")
    bot.logger.info("-------------------")
    status_task.start()
    if config["sync_commands_globally"]:
        bot.logger.info("Syncing commands globally...")
        await bot.tree.sync()

@tasks.loop(minutes=1.0)
async def status_task() -> None:
    """
    Setup the game status task of the bot.
    """
    statuses = ["processing maps", "under maintainence"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))


async def load_coordinates() -> None:
    """
    The code in this function is executed whenever the bot will start.
    """
    for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"cogs.{extension}")
                bot.logger.info(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                bot.logger.error(f"Failed to load extension {extension}\n{exception}")




async def load_bot() -> None:
    """
    The code in this function is executed after the initiation of bot
    """
    # TODO: take input as argparse of the input




asyncio.run(load_bot)