from .prompts import Prompt, Response, Action, ActionResponse

class Arena:
    def __init__(self, game):
        self.sections = [
            Snow(game), Mountains(game), Savanah(game),
            Forest(game), Cornucopia(game), Plains(game),
            RainForest(game), Grassland(game), Desert(game)
        ]
        

    def __getitem__(self, id):
        if id < 1 or id > len(self.sections):
            raise ValueError('Invalid section.')
        return self.sections[id-1]


class Section:
    id: int
    neighbours: list

    def __init__(self, game):
        self.game = game
        self.players = []

    def __repr__(self):
        return self.__class__.__name__

    def get_prompt(self, player) -> Prompt:
        return Prompt(f'lmao {player.name}', [Response('uwu', Action()), Response('uwu', Action())])

class Snow(Section):
    id = 1
    neighbours = [2, 4]

class Mountains(Section):
    id = 2
    neighbours = [1, 3, 5]

class Savanah(Section):
    id = 3
    neighbours = [2, 6]

class Forest(Section):
    id = 4
    neighbours = [1, 5, 7]

class Cornucopia(Section):
    id = 5
    neighbours = [2, 4, 8, 6]

class Plains(Section):
    id = 6
    neighbours = [3, 5, 9]

class RainForest(Section):
    id = 7
    neighbours = [4, 8]

class Grassland(Section):
    id = 8
    neighbours = [5, 7, 9]

class Desert(Section):
    id = 9
    neighbours = [6, 8]