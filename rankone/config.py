import os


GUILD = os.getenv('DISCORD_GUILD')
TOKEN = os.getenv('DISCORD_TOKEN')
ADMIN_ROLE = 'Admins'

monitored_reactions = {'🔴': 'Red', '🔵': 'Blue'}

# CHANNEL_ID(s) of channels that the bot will monitor match messages and match reaction events
MONITORED_CHANNELS = [752723109710266468]

# CHANNEL_ID of the channel where any channel level logs will go
LOG_CHANNEL = 752722021674123285
