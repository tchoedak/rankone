from .bot import bot
from .algorithms import configure_trueskill
from .config import TOKEN, TRUESKILL_SETTINGS


def start():
    configure_trueskill(**TRUESKILL_SETTINGS)
    bot.run(TOKEN)


if __name__ == '__main__':
    start()
