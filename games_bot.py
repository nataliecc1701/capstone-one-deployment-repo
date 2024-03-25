'''The Discord Bot section of the project'''

# python imports
import os

# library imports
import discord
from discord.ext import commands
from sqlalchemy import select, or_
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
        await show_board(message)
    elif message.content.startswith("$move"):
        if message.author.name not in selected_game:
            await message.channel.send("No game to move!")
            return
        game = selected_game[message.author.name]
        if len(message.content.split()) == 0:
            await message.channel.send("""syntax: $move [house number]
                                       house number starts at 1 and increases left to right""")
            return
        if message.content.split()[1].isdigit:
            house = int(message.content.split()[1])
            err = game.invalidate_move(house-1)
            if err:
                await message.channel.send(err)
            else:
                with Session(engine) as session:
                    mv = MancalaMove(match_id = game.id, move_number = game.move_count, player = game.turn, house = house)
                    query = (select(Match)
                                 .where(Match.id == game.id))
                    db_game = session.scalars(query).one()
                    turn_int = 1
                    if game.turn:
                        turn_int = 0
                    
                    session.add(mv)
                    try:
                        session.commit()
                    except:
                        await message.channel.send("error committing move to database")
                    status = game.move(house)
                    if status[0] >= 20:
                        await message.channel.send(status[1])
                    if status[0] == 10:
                        await message.channel.send("Move made, awaiting move by opposing player")
                        db_game.status_code = 11 + turn_int
                    if status[0] == 11:
                        await message.channel.send(game)
                    if status[0] == 12:
                        await message.channel.send("Game finished!")
                        lead = game.tally_lead()
                        if game.is_solitaire():
                            winner = "Challenged"
                            if lead == 0:
                                winner = "Challenger"
                            await message.channel.send(f"{winner} won!")
                        else:
                            if lead == turn_int:
                                await message.channel.send(f"You beat @{game.get_opponent()}!")
                            else:
                                await message.channel.send(f"@{game.get_opponent()} won!")
                        db_game.status_code = 21 + lead
                    session.add(db_game)
                    session.commit()
                    
                    if status[0] < 20 and status[0] != 11:
                        selected_game[message.author.name] = None
                        advance_game(message.author.name)
                        if message.author.name in selected_game:
                            await message.channel.send("Next game:")
                        await show_board(message)
                    
        else:
            await message.channel.send("need a house number to move")
    elif message.content.startswith("$listgames"):
        with Session(engine) as session:
            games = (select(Match)
                     .filter(or_(Match.challenged == message.author.name, Match.challenger == message.author.name))
                     .filter(Match.status_code < 20)
                     .order_by(Match.move_time.desc()))
            games_list = session.scalars(games).all()
            
            if not games_list:
                await message.channel.send("You have no active games")
            
            ready_list = []
            waiting_list = []
            for game in games_list:
                if game.challenged == game.challenger:
                    ready_list.append(f"Solitaire")
                elif game.challenged == message.author.name:
                    s = f"{game.challenger}"
                    if game.status_code in (10, 12):
                        ready_list.append(s)
                    else:
                        waiting_list.append(s)
                elif game.challenger == message.author.name:
                    s = f"{game.challenged}"
                    if game.status_code == 11:
                        ready_list.append(s)
                    else:
                        waiting_list.append(s)
            sendlist = []
            if ready_list:
                sendlist.append(f"Awaiting your move vs. {', '.join(ready_list)}")
            if waiting_list:
                sendlist.append(f"Awaiting opponents' moves vs. {', '.join(waiting_list)}")
            await message.channel.send("\n".join(sendlist))
    elif message.content.startswith("switchgame"):
        if len(message.content.split()) == 0:
            await message.channel.send("""syntax: $switchgame [opponent]
                                       opponent should be entered as it appears on $listgames command""")
            return
        opponent = message.content.split()[1]
        if opponent.lower() == "solitaire":
            opponent = message.author.name
        
        with Session(engine) as session:
            q = (select(Match)
                 .filter(or_
                         ((Match.challenged == message.author.name)&(Match.challenger == opponent),
                          (Match.challenged == opponent)&(Match.challenger == message.author.name)))
                 .filter(Match.status_code < 20)
                 .order_by(Match.move_time.desc()))
            
            game = session.scalars(q).first()
            
            if not game:
                await message.channel.send("No game vs that opponent")
            else:
                new_game = make_board(game)
            selected_game[message.author.name] = new_game
            show_board(message)


async def challenge(challenger, challenged, channel):
    """Challenges another user and adds that challenge to the database.
    If the user has no current board, sets their current board"""
    if challenged == client.user:
        await channel.send("You cannot challenge the bot")
        return
    
    with Session(engine) as session:
        q = (select(Match)
             .filter(or_
                     ((Match.challenged == challenged.name)&(Match.challenger == challenger.name)&(Match.status_code in [10, 12]),
                      (Match.challenged == challenger.name)&(Match.challenger == challenged.name)&(Match.status_code == 11)))
             .order_by(Match.move_time.desc()))
        
        existing = session.scalars(q).first()
        if existing:
            await channel.send("You cannot issue a second challenge against the same opponent while a game is active")
            return
        
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
                    return make_board(chalr)
                return make_board(chald)
            return make_board(chald)
        if chalr:
            return make_board(chalr)
        return None

def make_board(game):
    """Constructs a board from a database entry"""
    return MancalaBoard (id = game.id, moves = game.moves, challenger=game.challenger, challenged=game.challenged)

def advance_game(username):
    """Sets the user's selected game to their next game, or none if there are no games awaiting them."""
    game = get_next_game(username)
    if game:
        selected_game[username] = game

async def show_board(message):
    """Shows the user's current board"""
    game = None
    if message.author.name in selected_game:
        game = selected_game[message.author.name]
    else:
        advance_game(message.author.name)
        if message.author.name in selected_game:
            game = selected_game[message.author.name]
        else:
            await message.channel.send("There are no games waiting for you to move")
    if game:
        if game.is_solitaire():
            current = "Challenged"
            if game.turn:
                current = "Challenger"
            await message.channel.send(f"Solitaire ({current} side)")
        else:
            opponent = game.get_opponent()
            await message.channel.send(f"vs {opponent}")
        await message.channel.send(game)

client.run(os.environ['DISCORD_BOT_TOKEN'])