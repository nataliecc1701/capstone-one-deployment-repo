'''Database models for the discord bot. Current model just includes the mancala game'''

# python imports
from datetime import datetime

# SQLAlchemy library import
from sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Match(db.Model):
    '''Contains matches: when they were started, what game is being played,
    and which users are involved'''
    
    __tablename__ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True)
    
    challenger = db.Column(db.Text, nullable = False)
    # Discord identifier for the challenger
    
    challenged = db.Column(db.Text, nullable = False)
    # Discord identifier for the user challenged
    
    challenge_time = db.Column(db.DateTime, nullable = False, default = datetime.utcnow())
    
    game = db.Column(db.Integer, nullable = False, default = 0)
    # for now, includes an integer value corresponding to the game in question
    # A value of 0 corresponds to Kalah(6,4)
    
class MancalaMove(db.Model):
    '''Contains moves in a game of mancala: which player did it, and which of their houses
    did they move'''
    
    __tablename__ = 'mancala_moves'
    
    id = db.Column(db.Integer, primary_key = True)
    
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=False)
    move_number = db.Column(db.Integer)
    # Could use these as a composite primary key instead
    
    player = db.Column(db.Boolean, nullable=False, default=False)
    # TRUE if the move was made by the challenger, FALSE if made by the challenged
    
    house = db.Column(db.Integer, nullable=False)
    
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())