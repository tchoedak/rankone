'''
Contains parsing logic to take a message from a PUG game
and converts it to meangingful data so elo and elo gains can be
calculated
'''
from .player import Player, Team
from . import config


def is_match(message_content):
    '''
	Returns True if it is a match
	'''
    if 'teams have been selected:' in message_content.lower():
        return True
    else:
        return False


def is_monitored_match(mentions):
    '''
    Returns True if the number of mentions matches
    the number of expected players for monitored game modes
    otherwise returns False
    '''
    for game_mode in config.MONITORED_GAME_MODES:
        if len(mentions) == config.GAME_MODES_TO_PLAYERS[game_mode]:
            return True
    return False


def parse_match(message_id, content, mentions):
    '''
	parses players, teams, and match id from a message
	'''
    match_id = message_id
    players = []
    red_players = []
    blue_players = []
    for mention in mentions:
        players.append(Player(player_id=mention.id, name=mention.name))

    header, red_team_text, blue_team_text = content.split('\n')
    for player in players:
        if str(player.player_id) in red_team_text:
            red_players.append(player)
        if str(player.player_id) in blue_team_text:
            blue_players.append(player)

    teams = {'Red': Team(*red_players), 'Blue': Team(*blue_players)}
    return match_id, players, teams
