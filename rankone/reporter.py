from typing import Callable, Any, List
import random
from . import db
from .player import Player
from .config import BOT_MESSAGE_PREFIX


def as_bot(message: str) -> str:
    return BOT_MESSAGE_PREFIX + message


def bot_message(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
    def wrapper(*args, **kwargs):
        return as_bot(func(*args, **kwargs))

    return wrapper


@bot_message
def get_report(players: List[Player]) -> str:
    report = ', '.join(
        [f'{player.display_name}: {random.randint(900, 1700)}' for player in players]
    )
    return report


@bot_message
def get_elo_report(*players: Player, has_updated: bool = False) -> str:
    report = ', '.join(
        f'{player.display_name} [{player.elo:4.0f}]' for player in players
    )
    header = 'Elo updated! '
    if has_updated:
        report = header + report
    return report


@bot_message
def get_leader_report(players: List[Player]) -> str:
    # assumes players are already sorted in descending
    report = f'Top {len(players)} players: \n'
    for i, player in enumerate(players):
        report = report + f'{i+1}. {player.display_name} [{player.elo:4.0f}]\n'
    return report
