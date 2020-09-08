import os
import random
import logging

import discord
from discord.ext import commands

from logger import get_logger
from commands import Commands
import reporter
from elo import EloSystem
from algorithms import elo_gains_v1
import parser
import db
import config

logger = get_logger(logging.INFO)

bot = commands.Bot(command_prefix='.')
bot.add_cog(Commands(bot))
elo = EloSystem(algorithm=elo_gains_v1)


async def send_to_log_channel(message):
    log_channel = bot.get_channel(config.LOG_CHANNEL)

    await log_channel.send(message)


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=config.GUILD)

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
            db.show_db()
            db.show_players()
            await send_to_log_channel(
                f"Matched added! match_id: {match_id}\nRed: {teams['Red']}\nBlue: {teams['Blue']}"
            )


@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.channel.id in config.MONITORED_CHANNELS:
        winning_team = config.monitored_reactions.get(reaction.emoji)
        if winning_team:
            losing_team = (
                set(config.monitored_reactions.values()) - set([winning_team])
            ).pop()
            match_id = reaction.message.id
            db.set_winner(match_id, winning_team)
            db.show_db()

            match_id, players, teams = parser.parse_match(
                reaction.message.id, reaction.message.content, reaction.message.mentions
            )
            win_elo, lose_elo = elo.calculate_elo_gains(
                teams[winning_team], teams[losing_team]
            )
            db.update_player_elo(teams[winning_team].players, win_elo)
            db.update_player_elo(teams[losing_team].players, lose_elo)
            db.show_players()
            await reaction.message.channel.send(reporter.get_elo_report(players))
            await send_to_log_channel(
                f'Match updated!\nmatch_id: {match_id}. winner: {winning_team}. elo_gain: {win_elo:5.0f}'
            )
