import commands
from .bot import bot
from .config import TOKEN


def start():
    bot.run(TOKEN)


if __name__ == '__main__':
    start()
