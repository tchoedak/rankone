import os
import random
import logging

import discord
from discord.ext import commands

from logger import get_logger
from commands import Commands
from reporter import get_report


logger = get_logger(logging.INFO)

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')
bot.add_cog(Commands(bot))

'''
TODO:

Let's create an ELO system.

'''

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    logging.info(
        f'author: {message.author}\n'
        f'content: {message.content}\n'
        f'channel: {message.channel}\n'
        f'mentions: {message.mentions}\n'
        f'id: {message.id}\n'
        f'created_at: {str(message.created_at)}\n'
    )

    if 'teams have been selected:' in message.content.lower():
        await message.channel.send('match added')

    await message.channel.send(get_report([message.author]))
