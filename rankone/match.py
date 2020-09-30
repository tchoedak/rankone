from typing import Awaitable, Any, List, Callable
from discord import Message, Reaction
from . import parser
from . import config
from . import db
from . import utils
from . import reporter
from .elo import EloSystem
from .player import Player


class MatchManager(object):
    def __init__(self, elo_system: EloSystem):
        self.elo_system = elo_system

    def is_match(self, message: Message) -> bool:
        return (
            (message.channel.id in config.MONITORED_CHANNELS)
            and parser.is_monitored_match(message)
            and parser.is_match(message)
        )

    def is_match_reaction(self, reaction: Reaction) -> bool:
        return reaction.emoji in config.MONITORED_REACTIONS

    async def update_match(
        self, reaction: Reaction, callbacks: List[Callable[[Any], Any]]
    ):
        '''
        Handle a match updated through reaction event by parsing the match
        message, parsing the match winners, recalculating elo based on results,
        updating the database with adjusted elo, and reporting back to the channel
        of the updated elos.
        '''
        winning_team = config.MONITORED_REACTIONS.get(reaction.emoji)

        message = reaction.message
        match_id = message.id
        match_winner = db.get_match_winner(match_id)
        losing_team = (
            set(config.MONITORED_REACTIONS.values()) - set([winning_team])
        ).pop()

        # only proceed if the match hasn't already been recorded or if
        # the new match winner is not the existing marked winner
        if not match_winner or match_winner.team != winning_team:
            db.set_winner(match_id, winning_team)

            match_id, players, teams = parser.parse_match(message)

            winning_team, losing_team = self.elo_system.calculate_elo_gains(
                teams[winning_team], teams[losing_team]
            )

            db.update_player_elo(winning_team.players)
            db.update_player_elo(losing_team.players)

            updated_players = self.update_player_display_names(
                players, reaction.message
            )
            report = reporter.get_elo_report(*updated_players, has_updated=True)

            for callback in callbacks:
                await callback(reaction, report)

    def update_player_display_names(self, players: Player, message) -> List[Player]:
        '''
        Given a list of players, updates the player's display_name attribute.
        '''
        for player in players:
            player.display_name = utils.get_display_name(
                message.guild.members, player.player_id
            )
        return players

    async def add_match(self, message: Message, callbacks: List[Callable[[Any], Any]]):
        '''
        Handle a match added event by parsing the match message, parsing
        the teams and players, adding the match to the DB, and
        reporting back to the channel that the match has been added.
        '''
        await message.add_reaction(config.MATCH_REACTION)

        match_id, players, teams = parser.parse_match(message)
        match_created_at = message.created_at

        db.add_match(teams['Red'], teams['Blue'], match_id, match_created_at)
        db.register_players(teams['Red'].players + teams['Blue'].players)

        red_players = self.update_player_display_names(teams['Red'].players, message)
        blue_players = self.update_player_display_names(teams['Blue'].players, message)

        red_win_probability = get_team1_win_probability(teams['Red'], teams['Blue'])
        blue_win_probability = 1 - red_win_probability
        if red_win_probability > blue_win_probability:
            favored_team = 'Red'
            percent_win = red_win_probability * 100
        else:
            favored_team = 'Blue'
            percent_win = blue_win_probability * 100

        report = reporter.as_bot(
            f'Match added! match_id: {match_id}. '
            f'Red: {[player.display_name for player in red_players]}. '
            f'Blue: {[player.display_name for player in blue_players]}.'
            f'Probability of {favored_team} winning is {percent_win}%.'
        )

        for callback in callbacks:
            await callback(message, report)
