'''Database models for the discord bot. Current model just includes the mancala game'''

# python imports
from datetime import datetime
from typing import List, Optional
import os

# SQLAlchemy library import
from sqlalchemy import ForeignKey, String, DateTime, Boolean, Integer, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship
from sqlalchemy.sql import func

create_engine(os.environ["GAMES_BOT_DATABASE"], echo=True)

class Base(DeclarativeBase):
    pass

class Match(Base):
    '''Contains matches: when they were started, what game is being played,
    and which users are involved'''
    
    __tablename__ = 'matches'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    challenger: Mapped[str] = mapped_column(String(50))
    # Discord identifier for the challenger
    
    challenged: Mapped[str] = mapped_column(String(50))
    # Discord identifier for the user challenged
    
    challenge_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    game: Mapped[int] = mapped_column(Integer(), nullable=False, default = 0)
    # for now, includes an integer value corresponding to the game in question
    # A value of 0 corresponds to Kalah(6,4)
    
    moves: Mapped[List["MancalaMove"]] = relationship(
        back_populates="game", cascade="all, delete_orphan"
    )
    
class MancalaMove(Base):
    '''Contains moves in a game of mancala: which player did it, and which of their houses
    did they move'''
    
    __tablename__ = 'mancala_moves'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    match_id: Mapped[int] = mapped_column(ForeignKey('matches.id'), nullable=False)
    move_number: Mapped[int] = mapped_column(Integer(), nullable=False)
    # Could use these as a composite primary key instead
    
    player: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
    # TRUE if the move was made by the challenger, FALSE if made by the challenged
    
    house: Mapped[int] = (Integer())
    
    timestamp: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())