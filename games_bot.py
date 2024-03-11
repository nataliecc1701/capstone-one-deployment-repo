'''The Discord Bot section of the project'''

# python imports
import os

# library imports
import discord
from discord.ext import commands
from sqlalchemy import select
from sqlalchemy.orm import Session

# local imports
from mancala_logic import MancalaBoard
from models import Match, MancalaMove, engine

description = "A bot for playing simple board games between users. Currently only capable of playing mancala"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)

selected_game = dict() # Store active games in a dictionary
# selected_game[user_id] will be the game the bot is currently expecting
# the user indicated by user_id to make a move for

# Bot commands
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if not message.content.startswith("$"):
        return
    
    if message.content.startswith("$challenge") and len(message.mentions) == 1:
        await challenge(message.author, message.mentions[0], message.channel)
    elif message.content.startswith("$showboard"):
        if message.author.name in selected_game:
            await message.channel.send(selected_game[message.author.name])
        else:
            game = get_next_game(message.author.name)
            if game:
                selected_game[message.author.name] = game
                await message.channel.send(game)
            else:
                await message.channel.send("There are no games waiting for you to move")


async def challenge(challenger, challenged, channel):
    """Challenges another user and adds that challenge to the database.
    If the user has no current board, sets their current board"""
    if challenged == client.user:
        await channel.send("You cannot challenge the bot")
        return
    
    with Session(engine) as session:
        mtch = Match(challenger = challenger.name, challenged=challenged.name)
        
        session.add(mtch)
        session.commit()
        
        board = MancalaBoard(id=mtch.id)
        if not selected_game.get(challenged.name, None):
            selected_game[challenged.name] = board
        
    await channel.send(f"Challenging user {challenged.display_name} to a game of mancala")
            
def get_next_game(username):
    """Gets the game where it has most recently become the current user's turn.
    Returns None if there are none"""
    
    with Session(engine) as session:
        challenger_games = (select(Match)
                            .where(Match.challenger == username)
                            .where(Match.status_code == 11)
                            .order_by(Match.move_time.desc()))
        challenged_games = (select(Match)
                            .where(Match.challenged == username)
                            .where(Match.status_code.in_([10,12]))
                            .order_by(Match.move_time.desc()))
        
        chalr = session.scalars(challenger_games).one_or_none()
        chald = session.scalars(challenged_games).one_or_none()
        # probably a way to do this in SQL but I don't want to think about that this time of night
        
        if chald:
            if chalr:
                if chalr.move_time > chald.move_time:
                    return MancalaBoard(id = chalr.id, moves = chalr.moves)
                return MancalaBoard(id = chald.id, moves = chald.moves)
            return MancalaBoard(id = chald.id, moves = chald.moves)
        if chalr:
            return MancalaBoard(id = chalr.id, moves = chalr.moves)
        return None

client.run(os.environ['DISCORD_BOT_TOKEN'])