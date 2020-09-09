from rankone.player import Player, Team
from rankone.elo import EloSystem
from rankone.algorithms import elo_gains_v1
import math


def test_elo_gains_v1(balanced_teams, red_weaker):
    elo = EloSystem(elo_gains_v1)

    red, blue = balanced_teams
    win_elo, lose_elo = elo.calculate_elo_gains(red, blue)
    assert math.floor(win_elo) == 18
    assert math.floor(lose_elo) == -19

    red, blue = red_weaker
    win_elo, lose_elo = elo.calculate_elo_gains(red, blue)
    assert math.floor(win_elo) == 31
    assert math.floor(lose_elo) == -32
