import random
import db
from config import BOT_MESSAGE_PREFIX


def bot_message(func):
    def wrapper(*args):
        return BOT_MESSAGE_PREFIX + func(*args)

    return wrapper


@bot_message
def get_report(players):
    report = ', '.join(
        [f'{player.name}: {random.randint(900, 1700)}' for player in players]
    )
    return report


@bot_message
def get_elo_report(players):

    report = ', '.join(f'{player.name}: {player.elo:5.0f}' for player in players)
    header = 'Elo updated! '
    return header + report
