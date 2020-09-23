from discord import Message, Reaction
from . import config
from . import bot


async def send_to_reaction_channel(reaction: Reaction, report: str, **kwargs):
    await reaction.message.channel.send(report)


async def send_to_message_channel(message: Message, report: str, **kwargs):
    await message.channel.send(report)


async def send_to_log_channel(channel, report: str):
    log_channel = bot.bot.get_channel(config.LOG_CHANNEL)
    await log_channel.send(config.BOT_MESSAGE_PREFIX + report)
