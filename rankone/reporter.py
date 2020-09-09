import random
from . import db
from .config import BOT_MESSAGE_PREFIX


def as_bot(message):
    return BOT_MESSAGE_PREFIX + message


def bot_message(func):
    def wrapper(*args, **kwargs):
        return as_bot(func(*args, **kwargs))

    return wrapper


@bot_message
def get_report(players):
    report = ', '.join(
        [f'{player.name}: {random.randint(900, 1700)}' for player in players]
    )
    return report


@bot_message
def get_elo_report(*players, has_updated=False):

    report = ', '.join(f'{player.name} [{player.elo:4.0f}]' for player in players)
    header = 'Elo updated! '
    if has_updated:
        report = header + report
    return report


@bot_message
def get_leader_report(players):
    # assumes players are already sorted in descending
    report = f'Top {len(players)} players: \n'
    for i, player in enumerate(players):
        report = report + f'{i+1}. {player.name} [{player.elo}]\n'
    return report
