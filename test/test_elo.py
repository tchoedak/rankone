import pytest
from rankone.player import Player, Team
from rankone.elo import EloSystem


def test_teams(balanced_teams):

    Red, Blue = balanced_teams
    assert Red.combined_elo == 6050
    assert Red.average_elo == 1512.5
    assert Red.combined_weight == 500

    assert Blue.combined_elo == 6100
    assert Blue.average_elo == 1525
    assert Blue.combined_weight == 450


def test_elo_limiter(balanced_teams):
    low_gain = lambda a, b: (1, -50)
    low_loss = lambda a, b: (20, -1)
    red, blue = balanced_teams

    LIMIT = 5

    elo = EloSystem(low_gain, elo_gain_limit=5)
    win_elo, lose_elo = elo.calculate_elo_gains(red, blue)
    assert win_elo == 5
    assert lose_elo == -50

    elo = EloSystem(low_loss, elo_gain_limit=5)
    win_elo, lose_elo = elo.calculate_elo_gains(red, blue)
    assert win_elo == 20
    assert lose_elo == -5
