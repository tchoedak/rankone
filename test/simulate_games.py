import pytest
import random
import string
from rankone.player import Player, Team
from rankone import db, config
from rankone.elo import EloSystem
from rankone.algorithms import true_skill_ratings, trueskill, configure_trueskill


def pick_winning_team(player, other_players, does_player_win=True):
    winning_team = []
    losing_team = []
    if does_player_win:
        winning_team.append(player)
    else:
        losing_team.append(player)

    #
    random.shuffle(other_players)

    while len(winning_team) < 4:
        winning_team.append(other_players.pop())
    while len(losing_team) < 4:
        losing_team.append(other_players.pop())

    return Team(*winning_team), Team(*losing_team)


def get_random_name(length=7):
    letters = string.ascii_lowercase
    name = ''.join(random.choice(letters) for i in range(length))
    return name


def get_random_player():
    return Player(
        random.randint(1, 100),
        get_random_name(),
        elo=random.randint(1300, 1600),
        sigma=random.randint(50, 100),
    )


def simulate_one_player_path(starting_elo, starting_sigma, number_of_games, win_rate):
    kami = Player(3, 'kami', elo=starting_elo, sigma=starting_sigma)

    other_players = [get_random_player() for i in range(7)]

    ranker = EloSystem(algorithm=true_skill_ratings)
    for i in range(number_of_games):
        is_win = random.randint(0, 100) <= win_rate
        winning_team, losing_team = pick_winning_team(
            kami, [get_random_player() for i in range(7)], does_player_win=is_win
        )
        winner_results, loser_results = ranker.calculate_elo_gains(
            winning_team, losing_team
        )
    return kami


class Simulation(object):
    def __init__(
        self,
        starting_elo,
        starting_sigma,
        number_of_games,
        win_rate,
        number_of_simulations,
        ts_configs=None,
    ):
        self.starting_elo = starting_elo
        self.starting_sigma = starting_sigma
        self.win_rate = win_rate
        self.number_of_games = number_of_games
        self.number_of_simulations = number_of_simulations
        self.ts_configs = ts_configs or {}

    def simulate_one_player(self):
        configure_trueskill(**self.ts_configs)
        final_results = [
            simulate_one_player_path(
                self.starting_elo,
                self.starting_sigma,
                self.number_of_games,
                self.win_rate,
            )
            for i in range(self.number_of_simulations)
        ]
        return final_results

    def __repr__(self):
        return (
            f'Simulation(starting_elo: {self.starting_elo},'
            f' starting_sigma: {self.starting_sigma},'
            f' number_of_games: {self.number_of_games},'
            f' win_rate: {self.win_rate},'
            f' number_of_simulations: {self.number_of_simulations}'
            f' ts_configs: {self.ts_configs})'
        )

    def get_results(self):
        results = self.simulate_one_player()
        total_elo = sum([player.elo for player in results])
        average_elo = total_elo / len(results)
        print(self)
        print(f'Average elo after simulation: {average_elo}')
        return average_elo


if __name__ == '__main__':
    # high win rate, low number of games, default settings
    s1 = Simulation(
        starting_elo=1400,
        starting_sigma=100,
        number_of_simulations=10,
        number_of_games=3,
        win_rate=70,
    )
    s1.get_results()

    # average win rate, low number of games, default settings
    s2 = Simulation(
        starting_elo=1400,
        starting_sigma=100,
        number_of_simulations=10,
        number_of_games=3,
        win_rate=50,
    )
    s2.get_results()

    # high win rate, med number of games, default settings
    s3 = Simulation(
        starting_elo=1400,
        starting_sigma=100,
        number_of_simulations=10,
        number_of_games=13,
        win_rate=70,
    )
    s3.get_results()

    # average win rate, med number of games, default settings
    s4 = Simulation(
        starting_elo=1400,
        starting_sigma=100,
        number_of_simulations=10,
        number_of_games=13,
        win_rate=50,
    )
    s4.get_results()

    # very high win rate, med number of games, default settings
    s5 = Simulation(
        starting_elo=1400,
        starting_sigma=100,
        number_of_simulations=10,
        number_of_games=13,
        win_rate=80,
    )
    s5.get_results()

    # very high win rate, med number of games, high sigma, high beta
    s6 = Simulation(
        starting_elo=1400,
        starting_sigma=300,
        number_of_simulations=10,
        number_of_games=13,
        win_rate=80,
        ts_configs={'beta': 500},
    )
    s6.get_results()

    # high win rate, med number of games, high sigma, high beta
    s7 = Simulation(
        starting_elo=1400,
        starting_sigma=300,
        number_of_simulations=10,
        number_of_games=13,
        win_rate=70,
        ts_configs={'beta': 500},
    )
    s7.get_results()

    # average win rate, med number of games, high sigma, high beta
    s8 = Simulation(
        starting_elo=1400,
        starting_sigma=300,
        number_of_simulations=10,
        number_of_games=13,
        win_rate=50,
        ts_configs={'beta': 500},
    )
    s8.get_results()

    # decent win rate, large number of games, high sigma, high beta
    s9 = Simulation(
        starting_elo=1400,
        starting_sigma=300,
        number_of_simulations=10,
        number_of_games=100,
        win_rate=60,
        ts_configs={'beta': 500},
    )
    s9.get_results()

    # high win rate, large number of games, high sigma, high beta
    s10 = Simulation(
        starting_elo=1400,
        starting_sigma=300,
        number_of_simulations=10,
        number_of_games=100,
        win_rate=70,
        ts_configs={'beta': 500},
    )
    s10.get_results()
