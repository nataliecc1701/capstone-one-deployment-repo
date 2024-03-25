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
    elif message.content.startswith("$move"):
        if message.author.name not in selected_game:
            return
        game = selected_game[message.author.name]
        if message.content.split()[1].isdigit:
            house = int(message.content.split()[1])
            err = game.invalidate_move(house-1)
            if err:
                await message.channel.send(err)
            else:
                with Session(engine) as session:
                    mv = MancalaMove(match_id = game.id, move_number = len(game.moves), player = game.turn, house = house)
                    
                    session.add(mv)
                    try:
                        session.commit()
                    except:
                        await message.channel.send("error committing move to database")
                    status = game.move(house)
                    if status[0] >= 20:
                        await message.channel.send(status[1])
                    if status[0] == 11:
                        await message.channel.send(game)
                    if status[0] == 10 or status[0] == 12:
                        await message.channel.send("Move made, awaiting move by opposing player")
                        await message.channel.send("Next game:")
                        await message.channel.send(advance_game(message.author.username))
    elif message.content.startswith("$listgames"):
        await message.channel.send("Your current games are:")
    elif message.content.startswith("switchgame"):
        new_game = None # implement this
        selected_game[message.author.name] = new_game


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
        
        chalr = session.scalars(challenger_games).first()
        chald = session.scalars(challenged_games).first()
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

def advance_game(username):
    """Sets the user's selected game to their next game, or none if there are no games awaiting them.
    Returns a string that can be said as a reply by the bot"""
    game = get_next_game(username)
    if game:
        selected_game[username] = game
        return str(game)
    else:
        return "There are no games waiting for you to move"
    

client.run(os.environ['DISCORD_BOT_TOKEN'])