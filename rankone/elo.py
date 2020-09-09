from .algorithms import elo_gains_v1


class EloSystem:
    def __init__(self, algorithm=elo_gains_v1, elo_gain_limit=5):
        self.elo_cache = {'id': 0}  # only necessary if DB is too slow.
        self.algorithm = algorithm
        self.elo_gain_limit = elo_gain_limit

    def get_elo(self, player_id):
        return self.elo_db.get(player_id)

    def set_elo(self, player_id, elo):
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

    def calculate_elo_gains(self, winning_team, losing_team):
        '''
		Calculates elo gains for winning and losing teams using `EloSystem.algorithm`
		'''
        win_elo, lose_elo = self.algorithm(winning_team, losing_team)

        # ensure mins are met:
        win_elo = max(win_elo, self.elo_gain_limit)
        lose_elo = min(lose_elo, -self.elo_gain_limit)
        return win_elo, lose_elo
