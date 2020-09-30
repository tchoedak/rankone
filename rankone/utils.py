from datetime import datetime
import os
import subprocess
from typing import List
import itertools
import math

from discord import Member
from discord import utils as discord_utils

from .algorithms import trueskill
from . import db


class BackUp(object):
    def __init__(self, backup_id: str = None):
        self.backup_id = backup_id or datetime.now().strftime('%Y%m%d.%H.%M.%S')
        self.db_prefix = 'db.'
        self.backup_path = self.db_prefix + self.backup_id

    @property
    def exists(self) -> bool:
        return os.path.exists(self.backup_path)


def backup_db(backup_id: str = None) -> str:
    '''
    Backup the database.
    '''
    bk_up = BackUp(backup_id)
    cmd = ['cp', db.sqlite_db['database'], bk_up.backup_path]
    print(cmd)
    subprocess.call(cmd)
    return bk_up.backup_id


def restore_db(backup_id: str) -> str:
    '''
    Restore an existing database.
    '''
    bk_up = BackUp(backup_id)
    if bk_up.exists:
        new_bk_id = backup_db()
        restore_cmd = ['cp', bk_up.backup_path, db.sqlite_db['database']]
        result = subprocess.call(restore_cmd)
        if result == 0:
            response = f'New backup {new_bk_id} created. Backup {backup_id} restored.'
        else:
            response = 'Failed to restore backup'
    else:
        response = f'Backup {backup_id} does not exist'
    return response


def reset_db() -> int:
    '''
    Reset the database by removing the DB file and creating a new session.
    '''
    cmd = ['rm', db.sqlite_db['database']]
    result = subprocess.call(cmd) == 0
    db.session = db.get_session()
    return result


def get_display_name(members: List[Member], player_id: int) -> str:
    '''
    Get a player's discord display name from discord's API.
    '''
    member = discord_utils.get(members, id=player_id)
    return member.display_name


def get_team1_win_probability(team1, team2):
    '''
    Calculate the probability of `team1` winning against `team2.
    The formula is copied from https://trueskill.org/#win-probability
    '''
    delta_mu = sum(player.elo for player in team1.players) - sum(
        player.elo for player in team2.players
    )
    sum_sigma = sum(
        player.sigma ** 2 for player in itertools.chain(team1.players, team2.players)
    )
    size = len(team1.players) + len(team2.players)
    denom = math.sqrt(size * (trueskill.beta * trueskill.beta) + sum_sigma)
    return trueskill.cdf(delta_mu / denom)
