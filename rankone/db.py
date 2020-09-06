from datetime import datetime
import pandas as pd

from sqlalchemy.engine.url import URL
from sqlalchemy.schema import Column
from sqlalchemy.types import String, DateTime, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


STARTING_ELO = 1400

sqlite_db = {'drivername': 'sqlite', 'database': 'db.sqlite'}
engine = create_engine(URL(**sqlite_db))
_Session = sessionmaker()
_Session.configure(bind=engine)
session = _Session()

Base = declarative_base()


class Player(Base):
    __tablename__ = 'players'

    id = Column(String, primary_key=True)
    name = Column(String)
    elo = Column(Integer, default=1400)
    updated_at = Column(DateTime)


class Match(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer)
    player_id = Column(String)
    team = Column(String)
    win = Column(Boolean)
    match_created_at = Column(DateTime)
    created_at = Column(DateTime)


# create tables if not exists
Player.__table__.create(bind=engine, checkfirst=True)
Match.__table__.create(bind=engine, checkfirst=True)


def add_match(red, blue, message_id, match_created_at):
    '''
	Given a `red` and `blue` team and a `message_id` responsible for
	creating the match, add the match to the DB.
	'''
    now = datetime.now()

    for player in red.players:
        session.add(
            Match(
                player_id=player.player_id,
                team='Red',
                match_id=message_id,
                match_created_at=match_created_at,
                created_at=now,
            )
        )

    for player in blue.players:
        session.add(
            Match(
                player_id=player.player_id,
                team='Blue',
                match_id=message_id,
                match_created_at=match_created_at,
                created_at=now,
            )
        )
    session.commit()
    return True


def set_winner(match_id, winning_team):
    '''
	Given a match_id, set all players belonging to `winning_team` as winners.
	'''
    win = {'win': True}
    lose = {'win': False}

    session.query(Match).filter(Match.match_id == match_id).filter(
        Match.team == winning_team
    ).update(win)
    session.commit()
    session.query(Match).filter(Match.match_id == match_id).filter(
        Match.team != winning_team
    ).update(lose)
    return True


def get_match(match_id):
    '''
	Retrieve a match query result!
	'''
    match = session.query(Match).filter(Match.match_id == match_id)
    return match


def show_db():
    results = [result.__dict__ for result in db.session.query(db.Match).all()]
    df = pd.DataFrame(results)
    print(df[['match_id', 'player_id', 'team', 'win']])
