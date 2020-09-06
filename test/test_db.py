from datetime import datetime
import pytest


def test_add_match(db, balanced_teams):
    red, blue = balanced_teams
    match_one_id = 123456

    db.add_match(red, blue, match_one_id, datetime.now())
    db.set_winner(match_one_id, 'Blue')

    red_players = db.get_match(match_one_id).filter(db.Match.team == 'Red')
    for player_result in red_players:
        assert player_result.win is False

    assert len(red_players.all()) == len(red.players)

    blue_players = db.get_match(match_one_id).filter(db.Match.team == 'Blue')
    for player_result in blue_players:
        assert player_result.win is True

    assert len(blue_players.all()) == len(blue.players)

    match_two_id = 456789
    red, blue = balanced_teams

    db.add_match(red, blue, match_two_id, datetime.now())
    assert (
        len(db.session.query(db.Match.match_id).distinct(db.Match.match_id).all()) == 2
    )
    db.set_winner(match_two_id, 'Red')

    match_one_red_players = db.get_match(match_one_id).filter(db.Match.team == 'Red')
    for player_result in match_one_red_players:
        assert player_result.win is False

    red_players = db.get_match(match_two_id).filter(db.Match.team == 'Red')
    for player_result in red_players:
        assert player_result.win is True

    assert len(red_players.all()) == len(red.players)

    blue_players = db.get_match(match_two_id).filter(db.Match.team == 'Blue')
    for player_result in blue_players:
        assert player_result.win is False

    assert len(blue_players.all()) == len(blue.players)
