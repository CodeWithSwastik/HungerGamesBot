from .player import Tribute

class Game:
    def __init__(self):
        self.contestants = {}

    def add_contestant(self, member):
        c = Tribute.from_member(member)
        self.contestants[c.id] = c
