from typing import Callable, Tuple
from .player import Player, Team
from .algorithms import elo_gains_v1


class EloSystem:
    def __init__(
        self,
        algorithm: Callable[[Team, Team], Tuple[Team, Team]] = elo_gains_v1,
        elo_gain_limit: int = 5,
    ):
        self.elo_cache = {'id': 0}  # only necessary if DB is too slow.
        self.algorithm = algorithm
        self.elo_gain_limit = elo_gain_limit

    def get_elo(self, player_id: int):
        return self.elo_db.get(player_id)

    def set_elo(self, player_id: int, elo: float):
        self.elo_cache[player_id] = elo

    def persist_elos(self):
        '''
        TODO: implement a way to update the DB from the cache.
        '''
        raise NotImplementedError

    def refresh_elos(self):
        '''
        TODO: implement a way to refresh the cache from the DB.
        '''
        raise NotImplementedError

    def calculate_elo_gains(
        self, winning_team: Team, losing_team: Team
    ) -> Tuple[Team, Team]:
        '''
        Calculates elo gains for winning and losing teams using `EloSystem.algorithm`
        '''
        winning_team, losing_team = self.algorithm(winning_team, losing_team)

        return winning_team, losing_team
