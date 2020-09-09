from . import db


def avg(items):
    return sum(items) / len(items)


class Player(object):
    def __init__(self, player_id, name, elo=None, number_of_games=None):
        self.player_id = player_id
        self.name = name
        self._elo = elo
        self._number_of_games = number_of_games

    @property
    def elo(self):
        '''
        Returns the player's current Elo from ranked games
        '''
        if self._elo:
            return self._elo
        else:
            return db.get_player(self.player_id).elo

    @property
    def number_of_games(self):
        '''
        Returns the number of ranked games the player has played.
        '''
        return self._number_of_games

    def __str__(self):
        return f'<{self.name} id: {self.player_id}>'


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

    def __repr__(self):
        return ', '.join([str(player) for player in self.players])
