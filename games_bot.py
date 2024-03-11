'''The Discord Bot section of the project'''

# python imports
import os

# library imports
import discord
from discord.ext import commands

# local imports
from mancala_logic import MancalaBoard
from models import Match, MancalaMove

description = "A bot for playing simple board games between users. Currently only capable of playing mancala"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)

selected_game = dict() # Store active games in a dictionary
# selected_game[user_id] will be the game the bot is currently expecting a move for

# Bot commands
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if not message.content.startswith("$"):
        return
    
    if message.content.startswith("$"):
        await message.channel.send(f"Hello {message.author.display_name}")


client.run(os.environ['DISCORD_BOT_TOKEN'])