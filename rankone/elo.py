from .algorithms import elo_gains_v1


class EloSystem:

	def __init__(self, algorithm=elo_gains_v1, elo_gain_limit=5):
		self.elo_db = {
			'&748420734375821393': 1300,
			'@!124395956350353408': 1400,
		}
		self.algorithm = algorithm
		self.elo_gain_limit = elo_gain_limit

	def get_elo(self, player_id):
		return self.elo_db.get(player_id)

	def set_elo(self, player_id, elo):
		self.elo_db[player_id] = elo

	def calculate_elo_gains(self, winning_team, losing_team):
		win_elo, lose_elo = self.algorithm(winning_team, losing_team)

		# ensure mins are met:
		win_elo = max(win_elo, self.elo_gain_limit)
		lose_elo = min(lose_elo, -self.elo_gain_limit)
		return win_elo, lose_elo