import os
import random
import logging

from discord import Message, Reaction, User, utils as discord_utils
from discord.ext import commands

from .logger import get_logger
from .commands import Commands
from .elo import EloSystem
from .algorithms import true_skill_ratings
from . import reporter
from . import db
from . import config
from . import parser
from . import utils
from .callbacks import send_to_reaction_channel, send_to_message_channel
from .match import MatchManager


logger = get_logger(logging.INFO)

bot = commands.Bot(command_prefix='.')
bot.add_cog(Commands(bot))
true_skill_system = EloSystem(algorithm=true_skill_ratings)
match_manager = MatchManager(true_skill_system)


@bot.event
async def on_ready():
    guild = discord_utils.get(bot.guilds, id=config.GUILD_ID)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@bot.event
async def on_message(message: Message):
    if message.author == bot.user:
        return

    if config.DEBUG_MODE:
        logger.info(
            f'author: {message.author}\n'
            f'author_type: {type(message.author)}\n'
            f'content: {message.content}\n'
            f'content_type: {type(message.content)}\n'
            f'channel: {message.channel}\n'
            f'channel_type: {type(message.channel)}\n'
            f'mentions: {message.mentions}\n'
            f'mentions_type: {type(message.mentions)}\n'
            f'id: {message.id}\n'
            f'id_type: {type(message.id)}\n'
            f'created_at: {str(message.created_at)}\n'
            f'created_type: {type(message.created_at)}\n'
        )

    if message.channel.id in config.MONITORED_CHANNELS:
        await bot.process_commands(message)

        if match_manager.is_match(message):
            await match_manager.add_match(message, callbacks=[send_to_message_channel])


@bot.event
async def on_reaction_add(reaction: Reaction, user: User):
    if match_manager.is_match(reaction.message) and match_manager.is_match_reaction(
        reaction
    ):
        await match_manager.update_match(reaction, callbacks=[send_to_reaction_channel])
