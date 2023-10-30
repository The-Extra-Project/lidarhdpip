
import json
import os
import platform
import sys

sys.path.append(os.path.abspath('../../'))

import logging
import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context
from storage import Database
import aiosqlite
from bots.Discord.loggingFormatter import LoggingFormatter
from bots.consumer.kafkaConsumer import  kafka_consume_list_jobs
from bots.producer.kafkaProducer import  kafka_producer_job
from discord import app_commands

try:
    with open(f"{os.path.realpath(os.path.dirname(__file__))}/config.json") as file:
        config = json.load(file)
except FileNotFoundError as notFound:
    print(notFound)
    
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

bot: Bot = Bot(
command_prefix= "/circum",
intents=intents,
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



class Circumbot(commands.Bot):
    
    current_bw: int
    
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(config["prefix"]),
            intents=intents,
            help_command=None,
        )
        
        self.logger = logger
        self.config = config
        self.database = None
        self.current_bw = 0

    
    @bot.event
    async def setup_hook(self) -> None:
        """
        The code in this event is executed when the bot is deployed and incorporated by the main repo.
        """
        bot.logger.info(f"Logged in globally as {bot.user.name}")
        bot.logger.info(f"discord.py API version: {discord.__version__}")
        bot.logger.info(f"Python version: {platform.python_version()}")
        bot.logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
        bot.logger.info("-------------------")
       
        await self.init_db()
        await self.load_cogs()
        self.db = Database(
            connection= await aiosqlite.connect(
                 f"{os.path.realpath(os.path.dirname(__file__))}/storage/database.db"
            )
        )
        
    async def init_db(self):
        """
        initializes the database in order to store the user request along with the parameters
        """
        async with aiosqlite.connect(f"{os.path.realpath(os.path.dirname(__file__))}/storage/database.db") as db:
            with open(f"{os.path.realpath(os.path.dirname(__file__))}/storage/schema.sql") as _file:
                await db.executescript(_file.read())
            await db.commit()

    async def load_cogs(self):
        """
        sets up the user command template based on the various pipelines. 
        """   
        _file = os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs")
        # if _file.endswith(".py"):
        extension = _file[1] ## now selecting only UserCommands
        #     self.logger.info(extension)
        try:
            await self.load_extension(f"cogs.Commands")
            self.logger.info(f"loadded commands from '{extension}'")
        except Exception as e:
            self.logger.error(e
            )
    
    
    @bot.event
    async def on_message(self,message: discord.Message) -> None:
        """
        The code in this event is executed every time someone sends a message, with or without the prefix

        :param message: The message that was sent.
        """
        if message.author == self.user or message.author.bot:
            return
        
        try:
            await bot.process_commands(message)
        except Exception as e:
            print('message not able to be processed a cause de' + e)
       ## kafka_producer_job("demo", "1", "2", "ABCD", "oefzijfiojsdfj")
        await message.reply("hiya, check your job status")    
        

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
    
bot = Circumbot()
bot.run(token=config["token"])