'''The Discord Bot section of the project'''

# python imports
import os

# library imports
import discord
from discord.ext import commands

# local imports

description = "A bot for playing simple board games between users. Currently only capable of playing mancala"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='$', description=description, intents=intents)

# Bot commands



bot.run(os.environ['DISCORD_BOT_TOKEN'])