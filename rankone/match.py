class Match(object):
    def __init__(self, players, message_id, match_created_at):
        self.players = players
        self.match_id = message_id
        self.match_created_at = match_created_at
        self.red_players = None
        self.blue_players = None
        self.winning_team = Nones
