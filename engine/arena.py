from .prompts import Prompt, Response, ActionResponse, Message

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
        return Prompt(f'lmao {player.name}', [])

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cornucopia = []

    def get_prompt(self, player) -> Prompt:
        if player.responded:
            return 

        def enter():
            resp = ActionResponse(
                f'You entered the Cornucopia. These are the people there: {self.cornucopia}', 
                public=Message(f'{player.name} bravely enters the Cornucopia.')
            )
            self.cornucopia.append(player)
            return resp

        def run():
            return ActionResponse(
                'You ran away', 
                public=Message(f'{player.name} chooses to run away from the Cornucopia.')
            )

        responses = [
            Response(
                'Enter the Cornucopia', 
                action=enter, 
                id=0
            ), 
            Response(
                'Run away', 
                action=run, 
                id=1
            )
        ]
        return Prompt('Do you enter the Cornucopia?', responses)


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