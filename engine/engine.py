from .player import Player

class Game:
    def __init__(self):
        self.contestants = {}

    def add_contestant(self, member):
        c = Player.from_member(member)
        self.contestants[c.id] = c
