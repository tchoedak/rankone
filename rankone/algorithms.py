def threshold_elo_gains(team1, team2):
    threshold = 100

    team1_elo, team2_elo = 15, -15
    if team1.combined_weight < 100:
        team1_elo = 40

    if team2.combined_weight < 100:
        team2_elo = -40

    return team1_elo, team2_elo


def basic_elo_gains(team1, team2):
    return 15, -15


def elo_gains_v1(team1, team2):
    # team1 wins
    R1 = 10 ** (team1.combined_elo / 400)
    R2 = 10 ** (team2.combined_elo / 400)

    E1 = R1 / (R1 + R2)
    E2 = R2 / (R1 + R2)

    S1 = 1
    S2 = 0
    K = 130

    r1 = team1.combined_elo + K * (S1 - E1)
    r2 = team2.combined_elo + K * (S2 - E2)

    team1_shared_win = (r1 - team1.combined_elo) / len(team1.players)
    team2_shared_loss = (r2 - team2.combined_elo) / len(team2.players)

    return team1_shared_win, team2_shared_loss
