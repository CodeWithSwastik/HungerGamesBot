from .player import Player


class GameEngine:
    """The Internal Game Engine"""
    def __init__(self):
        self.contestants = {}

    def add_player(self, member):
        c = Player.from_member(member)
        self.contestants[c.id] = c