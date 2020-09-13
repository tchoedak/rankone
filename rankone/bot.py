import os
import random
import logging

import discord
from discord.ext import commands

from .logger import get_logger
from .commands import Commands
from .elo import EloSystem
from .algorithms import elo_gains_v1
from . import reporter
from . import db
from . import config
from . import parser


logger = get_logger(logging.INFO)

bot = commands.Bot(command_prefix='.')
bot.add_cog(Commands(bot))
elo = EloSystem(algorithm=elo_gains_v1)


async def send_to_log_channel(message):
    log_channel = bot.get_channel(config.LOG_CHANNEL)
    await log_channel.send(config.BOT_MESSAGE_PREFIX + message)


async def send_to_debug_channel(message):
    debug_channel = bot.get_channel(config.DEBUG_CHANNEL)
    await debug_channel.send(message)


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, id=config.GUILD_ID)

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    logging.info(
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
        if parser.is_match(message.content.lower()):
            match_id, players, teams = parser.parse_match(
                message.id, message.content, message.mentions
            )
            match_created_at = message.created_at
            db.add_match(teams['Red'], teams['Blue'], match_id, match_created_at)
            db.register_players(teams['Red'].players + teams['Blue'].players)
            match_added_message = reporter.as_bot(
                f"Matched added! match_id [{match_id}]. Red: {teams['Red']}. Blue: [{teams['Blue']}]"
            )
            if config.DEBUG_MODE:
                await send_to_debug_channel(match_added_message)
            else:
                await send_to_log_channel(
                    f"Matched added! match_id: [{match_id}]. Red: [{teams['Red']}]. Blue: [{teams['Blue']}]"
                )


@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.channel.id in config.MONITORED_CHANNELS:
        winning_team = config.monitored_reactions.get(reaction.emoji)
        if winning_team:

            match_id = reaction.message.id

            # check if match already has a winner
            match_winner = db.get_match_winner(match_id)
            if not match_winner or match_winner.team != winning_team:
                losing_team = (
                    set(config.monitored_reactions.values()) - set([winning_team])
                ).pop()
                db.set_winner(match_id, winning_team)

                match_id, players, teams = parser.parse_match(
                    reaction.message.id,
                    reaction.message.content,
                    reaction.message.mentions,
                )
                win_elo, lose_elo = elo.calculate_elo_gains(
                    teams[winning_team], teams[losing_team]
                )
                db.update_player_elo(teams[winning_team].players, win_elo)
                db.update_player_elo(teams[losing_team].players, lose_elo)

                elo_report_message = reporter.get_elo_report(*players, has_updated=True)
                match_updated_message = reporter.as_bot(
                    f'Match updated! match_id: [{match_id}]. winner: [{winning_team}]. elo_gain: [{win_elo:5.0f}]'
                )
                if config.DEBUG_MODE:
                    await send_to_debug_channel(elo_report_message)
                    await send_to_debug_channel(match_updated_message)
                else:
                    await reaction.message.channel.send(elo_report_message)
                    await send_to_log_channel(match_updated_message)
