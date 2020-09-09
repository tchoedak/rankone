import pytest
from rankone.player import Player, Team
from rankone import db


@pytest.fixture
def balanced_teams():
    nolja = Player(1, 'nolja', elo=1700, number_of_games=200)
    auron = Player(2, 'auron', elo=1500, number_of_games=140)
    kami = Player(3, 'kami', elo=1400, number_of_games=70)
    piece = Player(4, 'piece', elo=1450, number_of_games=90)

    lass = Player(5, 'lass', elo=1600, number_of_games=160)
    knell = Player(6, 'knell', elo=1550, number_of_games=70)
    vapor = Player(7, 'vapor', elo=1500, number_of_games=160)
    erz = Player(8, 'erz', elo=1450, number_of_games=60)

    Red = Team(nolja, auron, kami, piece)
    Blue = Team(lass, knell, vapor, erz)
    return Red, Blue


@pytest.fixture
def red_weaker():
    Red = Team(
        Player(9, 'damien', elo=1400, number_of_games=200),
        Player(10, 'bleil', elo=1450, number_of_games=200),
        Player(11, 'johnny', elo=1350, number_of_games=50),
        Player(12, 'grahamslam', elo=1425, number_of_games=100),
    )

    Blue = Team(
        Player(13, 'waisty', elo=1700, number_of_games=250),
        Player(14, 'monty', elo=1600, number_of_games=150),
        Player(15, 'vapor', elo=1500, number_of_games=180),
        Player(16, 'siv', elo=1500, number_of_games=200),
    )
    return Red, Blue
