from typing import Tuple
from .player import Team
from trueskill import TrueSkill


trueskill = TrueSkill()


def configure_trueskill(
    mu: float = None, sigma: float = None, beta: float = None, tau: float = None
):
    '''
    Configure `TrueSkill` with different settings.
    '''
    trueskill.mu = mu or trueskill.mu
    trueskill.sigma = sigma or trueskill.sigma
    trueskill.beta = beta or trueskill.beta
    trueskill.tau = tau or trueskill.tau


def threshold_elo_gains(team1: Team, team2: Team) -> Tuple(int, int):
    '''
    Returns 40, -40 elo gains IF the respective teams
    have less than 100 total combined games. Otherwise
    returns 15, -15.
    '''
    threshold = 100

    team1_elo, team2_elo = 15, -15
    if team1.combined_weight < 100:
        team1_elo = 40

    if team2.combined_weight < 100:
        team2_elo = -40

    return team1_elo, team2_elo


def basic_elo_gains(team1: Team, team2: Team) -> Tuple(int, int):
    return 15, -15


def elo_gains_v1(team1: Team, team2: Team) -> Tuple(int, int):
    '''
    Calculates using an ELO formula but does not take into account
    the number of games.
    '''
    # team1 wins
    R1 = 10 ** (team1.combined_elo / 400)
    R2 = 10 ** (team2.combined_elo / 400)

    E1 = R1 / (R1 + R2)
    E2 = R2 / (R1 + R2)

    S1 = 1
    S2 = 0
    K = 130  # adjust this number to affect elo boost

    r1 = team1.combined_elo + K * (S1 - E1)
    r2 = team2.combined_elo + K * (S2 - E2)

    team1_shared_win = (r1 - team1.combined_elo) / len(team1.players)
    team2_shared_loss = (r2 - team2.combined_elo) / len(team2.players)

    return team1_shared_win, team2_shared_loss


def true_skill_ratings(winning_team: Team, losing_team: Team) -> Tuple[Team, Team]:
    '''
    Returns winning team and losing team with adjusted ratings, elo, and sigma
    '''

    rankings = [0, 1]
    rating_groups = [winning_team.ratings, losing_team.ratings]

    winner_adjusted_ratings, loser_adjusted_ratings = trueskill.rate(
        rating_groups, rankings
    )
    for i, rating in enumerate(winner_adjusted_ratings):
        winning_team.players[i]._rating = rating
        winning_team.players[i]._elo = rating.mu
        winning_team.players[i]._sigma = rating.sigma

    for i, rating in enumerate(loser_adjusted_ratings):
        losing_team.players[i]._rating = rating
        losing_team.players[i]._elo = rating.mu
        losing_team.players[i]._sigma = rating.sigma

    return winning_team, losing_team
