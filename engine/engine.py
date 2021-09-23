from .player import Player
from .arena import Arena

class GameEngine:
    """The Internal Game Engine"""
    def __init__(self):
        self.players = {}
        self.arena = Arena()
        self.current_day = None

        self.prompts = {}
        self.responses = {}

    def add_player(self, member):
        c = Player.from_member(member)
        self.players[c.id] = c

    def setup(self):
        for player in self.players.values():
            player.location = self.arena[5]
            self.arena[5].players.append(player)

    def start_day(self, day):
        self.current_day = Day(day)

    def progress_day(self, time=10):
        self.current_day.time += time

    def end_day(self):
        self.current_day = None
        for player in self.players.values():
            player.reset_responses()


class Day:
    def __init__(self, date):
        self.date = date
        self.time = 0 # 0 - Morning | 100 - Night 


    def __repr__(self):
        if self.time < 33:
            return 'Morning'
        elif self.time < 66:
            return 'Afternoon'
        elif self.time < 99:
            return 'Evening'
        else:
            return 'Night'