import os


GUILD_ID = int(os.getenv('DISCORD_GUILD_ID'))
TOKEN = os.getenv('DISCORD_TOKEN')
ADMIN_ROLE = os.getenv('DISCORD_ADMIN_ROLE')

MONITORED_REACTIONS = {'🔴': 'Red', '🔵': 'Blue'}
MATCH_REACTION = "\U00002694"  # Unicode for :crossed_swords:

# CHANNEL_ID(s) of channels that the bot will monitor match messages and match reaction events
MONITORED_CHANNELS = [
    int(channel_id) for channel_id in os.getenv('DISCORD_MONITORED_CHANNELS').split(',')
]

GAME_MODES_TO_PLAYERS = {'5v5': 10, '4v4': 8, '3v3': 6, '2v2': 4, '1v1': 2}
MONITORED_GAME_MODES = ['4v4']

STARTING_ELO = 1400
STARTING_SIGMA = 200
TRUESKILL_SETTINGS = {'beta': 500}  # this was chosen from simulations


# CHANNEL_ID of the channel where any channel level logs will go
LOG_CHANNEL = int(os.getenv('DISCORD_LOG_CHANNEL'))

# The Bot will always prefix every message it sends to a channel with this prefix.
# This is used to make it easy to distinguish bot messages from other bots or from real users.
BOT_MESSAGE_PREFIX = ':robot: '

DEBUG_MODE = os.getenv('DISCORD_DEBUG_MODE') == 'ENABLED'
DEBUG_CHANNEL = int(os.getenv('DISCORD_DEBUG_CHANNEL'))
