import pytest
from rankone.player import Player, Team


@pytest.fixture
def balanced_teams():
    nolja = Player('1', 1700, 200)
    auron = Player('2', 1500, 140)
    kami = Player('3', 1400, 70)
    piece = Player('4', 1450, 90)

    lass = Player('5', 1600, 160)
    knell = Player('6', 1550, 70)
    vapor = Player('7', 1500, 160)
    erz = Player('8', 1450, 60)

    Red = Team(nolja, auron, kami, piece)
    Blue = Team(lass, knell, vapor, erz)
    return Red, Blue


@pytest.fixture
def red_weaker():
    Red = Team(
        Player('1', 1400, 200),
        Player('2', 1450, 200),
        Player('3', 1350, 50),
        Player('4', 1425, 100),
    )

    Blue = Team(
        Player('5', 1700, 250),
        Player('6', 1600, 150),
        Player('7', 1500, 180),
        Player('8', 1500, 200),
    )
    return Red, Blue


@pytest.fixture(scope='function')
def db():
    from rankone import db

    yield db
