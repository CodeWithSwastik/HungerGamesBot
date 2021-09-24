import random
from .prompts import Prompt, Response, ActionResponse, Message
from .weapon import generate_unique_weapons

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

    def move_player(player, section):
        player.location.players.remove(player)
        player.location = section
        section.players.append(player)

class Section:
    id: int
    neighbours: list

    def __init__(self, game):
        self.game = game
        self.players = []

    def __repr__(self):
        return self.__class__.__name__

    def get_prompt(self, player) -> Prompt:
        return Prompt(f'Default message {player.name}', [])

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
                f'You enter the Cornucopia. You come across some weapons and food.', 
                public=Message(f'{player.name} bravely enters the Cornucopia.'),
                followup=self.generate_weapon_prompt(player)
            )
            self.cornucopia.append(player)
            #player.finished_responding = True
            return resp

        def run():
            r = random.randint(1, 100)
            if r > 30:
                response = ActionResponse(
                    'You ran away', 
                    public=Message(f'{player.name} chooses to run away from the Cornucopia.')
                )
            elif r > 27: # 3% chance
                self.game.kill(player, 'stepped on a landmine')
                response = ActionResponse(
                    'You try to ran away but step on a landmine and die.', 
                    public=Message(f'{player.name} tries to run away but steps on a landmine and dies.')
                )
            else:
                player.health -= 10
                response = ActionResponse(
                    "You try to ran away but an arrow hits your leg and you can't run away. You'll need to fight to survive.", 
                    public=Message(f"{player.name} tries to run away but gets injured.")
                )
            player.finished_responding = True                   
            return response

        responses = [
            Response(
                'Enter the Cornucopia', 
                action=enter, 
            ), 
            Response(
                'Run away', 
                action=run, 
            )
        ]

        
        return Prompt('Do you enter the Cornucopia?', responses)

    def generate_weapon_prompt(self, player):
        def give_weapon(weapon):
            def inner():
                player.weapons.append(weapon)
                if len(self.cornucopia) > 1:
                    return ActionResponse(
                        f'You took the {weapon.name}. You see some people in the cornucopia, who do you attack?', 
                        followup=self.generate_choose_target_prompt(player)
                    )
                else:
                    return ActionResponse(
                        f'You took the {weapon.name}. It seems like you are the first one here.', 
                    )

            return inner

        responses = [
            Response(
                w.name, 
                emoji=w.emoji,
                action=give_weapon(w), 
            ) for w in generate_unique_weapons(random.randint(3,5))
        ]

        return player.create_prompt('Which weapon do you pick?', responses)

    def generate_choose_target_prompt(self, player):
        def attack(p):
            def inner():
                battle = self.game.start_battle(player, p)
                return ActionResponse(
                    f'You started a battle with {p.name}',
                    battle = battle
                )
            return inner

        responses = [
            Response(
                p.name, 
                emoji="💀",
                action=attack(p), 
            ) for p in self.cornucopia if p.id != player.id
        ]
        return player.create_prompt('Who do you attack?', responses)


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