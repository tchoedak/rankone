from datetime import datetime
import pandas as pd
import uuid
from typing import List

from sqlalchemy.engine.url import URL
from sqlalchemy.schema import Column
from sqlalchemy.types import String, DateTime, Boolean, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update


from . import config
from .player import Team


sqlite_db = {'drivername': 'sqlite', 'database': 'db.sqlite'}

Base = declarative_base()


class Player(Base):
    __tablename__ = 'players'

    id = Column(String, primary_key=True)
    name = Column(String)
    elo = Column(Integer, default=config.STARTING_ELO)
    sigma = Column(Float, default=config.STARTING_SIGMA)
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


def get_session():
    engine = create_engine(URL(**sqlite_db))
    _Session = sessionmaker()
    _Session.configure(bind=engine)

    # create tables if not exists
    Player.__table__.create(bind=engine, checkfirst=True)
    Match.__table__.create(bind=engine, checkfirst=True)
    return _Session()


session = get_session()


def add_match(
    red: Team, blue: Team, message_id: int, match_created_at: datetime
) -> bool:
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


def set_winner(match_id: int, winning_team: str) -> bool:
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
    session.commit()
    return True


def get_match(match_id: int) -> Match:
    match = session.query(Match).filter(Match.match_id == match_id)
    return match


def get_match_winner(match_id: int) -> Match:
    match = get_match(match_id)
    winner = match.filter(Match.win == True).distinct().first()
    return winner


def get_player(player_id: int) -> Player:
    player = session.query(Player).filter(Player.id == player_id).first()
    return player


def add_player(player_id: int, name: str) -> Player:
    player = Player(id=player_id, name=name, updated_at=datetime.now())
    session.add(player)
    session.commit()
    return player


def show_db():
    results = [result.__dict__ for result in session.query(Match).all()]
    df = pd.DataFrame(results)
    print(df[['match_id', 'player_id', 'team', 'win']])


def show_players():
    results = [result.__dict__ for result in session.query(Player).all()]
    df = pd.DataFrame(results)
    print(df[['id', 'name', 'elo', 'sigma']])


def register_players(players: Player) -> bool:
    '''
    Checks if players exist in Player table. If not, adds them to the Player table.
    '''
    for player in players:
        instance = session.query(Player).filter(Player.id == player.player_id).first()
        if not instance:
            p = Player(id=player.player_id, name=player.name, updated_at=datetime.now())
            session.add(p)
            session.commit()
    return True


def update_player_elo(players: List[Player]) -> bool:
    '''
    Updates the database with the latest player.elo, and player.sigma
    for every player in `players`.
    '''
    for player in players:
        db_player = session.query(Player).filter(Player.id == player.player_id).first()
        if db_player:
            db_player.elo = player.elo
            db_player.sigma = player.sigma
            session.commit()
    return True


def reset_all_elo() -> bool:
    '''
    Reset elo and sigma for ALL players.
    '''
    session.execute(
        update(
            Player.__table__,
            values={
                Player.__table__.c.elo: config.STARTING_ELO,
                Player.__table__.c.sigma: config.STARTING_SIGMA,
            },
        )
    )
    session.commit()
    return True


def get_top_n_players(n: int) -> List[Player]:
    top_players = session.query(Player).order_by(Player.elo.desc()).limit(n)
    return top_players.all()


def get_bottom_n_players(n: int) -> List[Player]:
    bottom_players = session.query(Player).order_by(Player.elo.asc()).limit(n)
    return bottom_players.all()
