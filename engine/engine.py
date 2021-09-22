from .player import Player
from .arena import Arena

class GameEngine:
    """The Internal Game Engine"""
    def __init__(self):
        self.players = {}
        self.arena = Arena()

    def add_player(self, member):
        c = Player.from_member(member)
        self.players[c.id] = c

    def setup(self):
        for player in self.players.values():
            player.location = self.arena[5]
            self.arena[5].players.append(player)