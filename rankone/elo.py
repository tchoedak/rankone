

class ELoSystem:

	def __init__(self):
		self.elo_db = {
			'&748420734375821393': 1300,
			'@!124395956350353408': 1400,
		}

	def get_elo(self, player_id):
		return self.elo_db.get(player_id)


	def set_elo(self, player_id, elo):
		return self.elo_db[player_id] = elo

	def calculate_elo_gains(self, team1, team2, weight_booster=0.8):
		'''
		Calculates the potential elo gains of team1 and team2 where the gains are
		weighted by a weight_booster.

		a bigger weight booster allots more gains
		'''
		team1_confidence = team1.average_elo/ (team1.combined_weight * (1 - weight_booster))
		team2_confidence = team2.average_elo/ (team2.combined_weight * (1 - weight_booster))

		team1_win_elo = min(5, (team2_average_elo - team1_average_elo) / (team1.combined_weight * (1 - weight_booster)))
		team2_win_elo = min(5, (team1_average_elo - team2_average_elo) / (team1.combined_weight * (1 - weight_booster)))

		return team1_win_elo, team2_win_elo