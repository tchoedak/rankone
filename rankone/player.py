from typing import List
from trueskill import Rating
from . import db


def avg(items: List[int]) -> float:
    return sum(items) / len(items)


class Player(object):
    def __init__(
        self,
        player_id: int,
        name: str,
        elo: int = None,
        number_of_games: int = None,
        rating: Rating = None,
        sigma: float = None,
    ):
        self.player_id = player_id
        self.name = name
        self._elo = elo
        self._number_of_games = number_of_games
        self._sigma = sigma
        self._rating = rating

    @property
    def elo(self) -> int:
        '''
        Returns the player's current Elo from ranked games
        '''
        if self._elo:
            return self._elo
        else:
            return db.get_player(self.player_id).elo

    @property
    def number_of_games(self) -> int:
        '''
        Returns the number of ranked games the player has played.
        '''
        return self._number_of_games

    def __str__(self):
        return f'<{self.name} id: {self.player_id}>'

    @property
    def sigma(self) -> float:
        if self._sigma:
            return self._sigma
        else:
            return db.get_player(self.player_id).sigma

    @property
    def rating(self) -> Rating:
        if self._rating:
            return self._rating
        else:
            return Rating(mu=self.elo, sigma=self.sigma)


class Team(object):
    '''
    Holds variable amount of players that make up a team.
    '''

    def __init__(self, *players):
        self.players = players

    @property
    def combined_elo(self) -> int:
        return sum([player.elo for player in self.players])

    @property
    def average_elo(self) -> float:
        return avg([player.elo for player in self.players])

    @property
    def combined_weight(self) -> int:
        return sum([player.number_of_games for player in self.players])

    @property
    def ratings(self) -> List[Rating]:
        return [player.rating for player in self.players]

    def __repr__(self) -> str:
        return ', '.join([str(player) for player in self.players])
