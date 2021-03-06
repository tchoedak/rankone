import random
import discord
from discord.ext import commands

from . import db
from . import config
from . import utils
from . import reporter
from . import version


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.log_channel = bot.get_channel(config.LOG_CHANNEL)

    @commands.command(name='show_matches')
    async def show_matches(self, ctx):
        db.show_db()

    @commands.command(name='show_players')
    async def show_players(self, ctx):
        db.show_players()

    @commands.command(name='backup_db')
    @commands.has_any_role(config.ADMIN_ROLE)
    async def backup_db(self, ctx, backup_id: str = None):
        backup_id = utils.backup_db(backup_id)
        await ctx.send(reporter.as_bot(f'Backup created! backup_id: {backup_id}'))

    @commands.command(name='restore_db')
    @commands.has_any_role(config.ADMIN_ROLE)
    async def restore_db(self, ctx, backup_id: str):
        response = utils.restore_db(backup_id)
        await ctx.send(reporter.as_bot(response))

    @commands.command(name='reset_db')
    @commands.has_any_role(config.ADMIN_ROLE)
    async def reset_db(self, ctx):
        backup_id = utils.backup_db()
        response = f'Backup {backup_id} created first before resetting elo\n'
        if utils.reset_db():
            response = response + 'DB reset.'
        else:
            response = response = 'Unable to reset DB'
        await ctx.send(reporter.as_bot(response))

    @commands.command(name='myelo')
    async def myelo(self, ctx):
        player_id, name = ctx.author.id, ctx.author.name
        player = db.get_player(player_id)
        if player:
            player.display_name = utils.get_display_name(
                ctx.guild.members, player_id=int(player_id)
            )
            report = reporter.get_elo_report(player)
        else:
            player = db.add_player(player_id, name)
            player.display_name = utils.get_display_name(
                ctx.guild.members, player_id=int(player_id)
            )
            report = reporter.get_elo_report(player)
        await ctx.send(report)

    @commands.command(name='elo')
    async def elo(self, ctx):
        player_ids = [mention.id for mention in ctx.message.mentions]
        if player_ids:
            players = list(
                filter(None, [db.get_player(player_id) for player_id in player_ids])
            )
            for player in players:
                player.display_name = utils.get_display_name(
                    ctx.guild.members, player_id=int(player.id)
                )
            if players:
                report = reporter.get_elo_report(*players)
            else:
                report = reporter.as_bot("Players don't exist")

            await ctx.send(report)

    @commands.command(name='reset_elo')
    @commands.has_any_role(config.ADMIN_ROLE)
    async def reset_elo(self, ctx):
        backup_id = utils.backup_db()
        await ctx.send(
            reporter.as_bot(f'Backup {backup_id} created first before resetting elo\n')
        )
        if db.reset_all_elo():
            response = 'Elo reset successful'
        else:
            response = 'Elo reset unsuccessful'
        await ctx.send(reporter.as_bot(response))

    @commands.command(name='elo_leaders')
    async def elo_leaders(self, ctx):
        top_limit = 10
        leaders = db.get_top_n_players(top_limit)
        for player in leaders:
            player.display_name = utils.get_display_name(
                ctx.guild.members, player_id=int(player.id)
            )
        await ctx.send(reporter.get_leader_report(leaders))

    @commands.command(name='elo_loser')
    async def elo_loser(self, ctx):
        loser = random.choice(
            [
                'f00l',
                'US stock market',
                'LA Clippers',
                'Boston Celtics',
                'You',
                'Disneys Mulan',
            ]
        )
        await ctx.send(reporter.as_bot(loser))

    @commands.command(name='elo_losers')
    async def elo_losers(self, ctx):
        bottom_limit = 10
        losers = db.get_bottom_n_players(bottom_limit)
        for player in losers:
            player.display_name = utils.get_display_name(
                ctx.guild.members, player_id=int(player.id)
            )
        await ctx.send(reporter.get_leader_report(losers))

    @commands.command(name='version')
    async def version(self, ctx):
        await ctx.send(reporter.as_bot(version.VERSION))
