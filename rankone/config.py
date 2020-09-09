import os


GUILD = os.getenv('DISCORD_GUILD')
TOKEN = os.getenv('DISCORD_TOKEN')
ADMIN_ROLE = 'Admins'

monitored_reactions = {'🔴': 'Red', '🔵': 'Blue'}

# CHANNEL_ID(s) of channels that the bot will monitor match messages and match reaction events
MONITORED_CHANNELS = [752723109710266468]

# CHANNEL_ID of the channel where any channel level logs will go
LOG_CHANNEL = 752722021674123285

# The Bot will always prefix every message it sends to a channel with this prefix.
# This is used to make it easy to distinguish bot messages from other bots or from real users.
BOT_MESSAGE_PREFIX = ':robot: '
