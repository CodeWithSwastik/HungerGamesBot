import random

from .player import Player
from .battle import Battle
from .arena import Arena

class GameEngine:
    """The Internal Game Engine"""
    def __init__(self):
        self.players = {}
        self.arena = Arena(self)
        self.current_day = None

        self.prompts = {}
        self.responses = {}

        self.finished = False
        self.winner = None

    def add_player(self, member):
        c = Player.from_member(member)
        self.players[c.id] = c

    @property
    def alive_players(self):
        return [m for m in self.players.values() if not m.dead]

    def setup(self):
        for player in self.players.values():
            player.location = self.arena[5]
            self.arena[5].players.append(player)

    def start_day(self, day):
        self.current_day = Day(day)

    def progress_day(self, time=60):
        self.current_day.time += time
        if all([p.finished_responding for p in self.alive_players]):
            self.end_day()        
            return False
        if len(self.alive_players) <= 1:
            self.end_day()        
            return False            

        for p in self.alive_players:
            p.update_hunger_and_thirst()
            if p.dead:
                self.kill(p, p.get_death_reason())

        return True

    def end_day(self):
        for player in self.players.values():
            player.reset_responses()
        
        if len(self.alive_players) == 1:
            self.finished = True
            self.winner = self.alive_players[0]
        elif len(self.alive_players) == 0:
            self.finished = True

    def add_response(self, player, response):
        response = self.players[player].add_response(response)
        return response.action()

    def kill(self, player, reason):
        player.kill(reason)
        self.current_day.killed.append(player)
        if hasattr(self, 'on_player_death'):
            self.on_player_death(player, reason)
        return reason

    def start_battle(self, player1, player2):
        if player1.in_battle or player2.in_battle:
            return False
        return Battle(self, player1, player2)

class Day:
    def __init__(self, date):
        self.date = date
        self.time = 0 # mins from 8 am
        self.length = random.randint(13, 15) # 9pm/10pm/11pm
        self.killed = [] # People that were killed


    def __repr__(self):
        if self.time < 4*60:
            return f'{8 + self.time//60} am (morning)'
        elif self.time < 8*60:
            return f'{(-4 + self.time//60) or "12:30"} pm (afternoon)'
        elif self.time < 12*60:
            return f'{-4 + self.time//60} pm (evening)'
        else:
            return f'{-4 + self.time//60} pm (night)'
