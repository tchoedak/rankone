import random
import discord
from discord.ext import commands

from . import db
from . import config
from . import utils


# these aren't working WTF?


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.log_channel = bot.get_channel(config.LOG_CHANNEL)

    @commands.command(name='roll_dice')
    async def roll_dice(self, ctx, number_of_dice: int, number_of_sides: int):
        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
        await ctx.send(', '.join(dice))

    @commands.command(name='create_channel')
    async def create_channel(self, ctx, channel_name='real-python'):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            print(f'Creating a new channel: {channdel_name}')
            await guild.create_text_channel(channel_name)

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
        await ctx.send(f'Backup created! backup_id: {backup_id}')

    @commands.command(name='restore_db')
    @commands.has_any_role(config.ADMIN_ROLE)
    async def restore_db(self, ctx, backup_id: int):
        pass
