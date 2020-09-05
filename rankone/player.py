def avg(items):
    return sum(items) / len(items)


class Player(object):
    def __init__(self, player_id, elo=None, number_of_games=None):
        self.player_id = player_id
        self._elo = elo
        self._number_of_games = number_of_games

    @property
    def elo(self):
        '''
		Returns the player's current Elo from ranked games
		'''
        return self._elo

    @property
    def number_of_games(self):
        '''
		Returns the number of ranked games the player has played.
		'''
        return self._number_of_games

    def boosted_elo(self, elo_gain):
        '''
		Returns the player's Elo adjusted for the elo_gain
		'''
        return self.elo + elo_gain


class Team(object):
    '''
	Holds variable amount of players that make up a team.
	'''

    def __init__(self, *players):
        self.players = players

    @property
    def combined_elo(self):
        return sum([player.elo for player in self.players])

    @property
    def average_elo(self):
        return avg([player.elo for player in self.players])

    @property
    def combined_weight(self):
        return sum([player.number_of_games for player in self.players])
