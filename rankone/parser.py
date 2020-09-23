'''
Contains parsing logic to take a message from a PUG game
and converts it to meangingful data so elo and elo gains can be
calculated
'''
from typing import Tuple, List
from discord import Message
from .player import Player, Team
from . import config


def is_match(message: Message) -> bool:
    '''
    Returns true if the message content resembles that of a PUG match
    '''
    if 'teams have been selected:' in message.content.lower():
        return True
    else:
        return False


def is_monitored_match(message: Message) -> bool:
    '''
    Returns True if the number of mentions matches
    the number of expected players for monitored game modes
    otherwise returns False
    '''
    for game_mode in config.MONITORED_GAME_MODES:
        if len(message.mentions) == config.GAME_MODES_TO_PLAYERS[game_mode]:
            return True
    return False


def parse_match(message: Message) -> Tuple[int, List[Player], dict]:
    '''
    parses players, teams, and match id from a message
    '''
    match_id = message.id
    content = message.content
    mentions = message.mentions

    players, red_players, blue_players = [], [], []

    for mention in mentions:
        players.append(Player(player_id=mention.id, name=mention.name))

    # Assumes a new line separates header from red team and from blue team
    header, red_team_text, blue_team_text = content.split('\n')
    for player in players:
        if str(player.player_id) in red_team_text:
            red_players.append(player)
        if str(player.player_id) in blue_team_text:
            blue_players.append(player)

    teams = {'Red': Team(*red_players), 'Blue': Team(*blue_players)}
    return match_id, players, teams
