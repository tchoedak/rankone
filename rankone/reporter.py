import random
import db


def get_report(players):
    report = ', '.join(
        [f'{player.name}: {random.randint(900, 1700)}' for player in players]
    )
    return report


def get_elo_report(players):

    report = ', '.join(f'{player.name}: {player.elo:5.0f}' for player in players)
    return report
