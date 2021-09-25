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

    def move_player(self, player, section):
        player.location.players.remove(player)
        player.location = section
        section.players.append(player)

class Section:
    id: int
    neighbours: list
    thirst: float # Multipier at which thirst increases in this Section
    hunger: float # Multipier at which hunger increases in this Section

    def __init__(self, game):
        self.game = game
        self.players = []

    def __repr__(self):
        return f'Section {self.id}: The {self.__class__.__name__}'

    def get_prompt(self, player) -> Prompt:
        return self.generic_prompt(player)

    def generic_prompt(self, player):
        
        section = self.game.arena[random.choice(self.neighbours)]

        def move():   
            player.finished_responding = True            
             
            self.game.arena.move_player(player, section)
            return ActionResponse(f'You moved to {section}')

        def food():
            player.finished_responding = True            

            if self.hunger > random.uniform(0, 5):
                return ActionResponse("You didn't find any food :/")
            else:
                player.hunger = 50 if player.hunger > 50 else 0
                return ActionResponse("You found some food")

        def water():
            player.finished_responding = True            

            if self.thirst > random.uniform(0, 5):
                return ActionResponse("You didn't find any water")
            else:
                player.thirst = 50 if player.hunger > 50 else 0
                return ActionResponse("You found some water")

        responses = [
            Response(
                f'Move to {section}', 
                emoji='🗺',
                action=move, 
            ), 
            Response(
                'Search for food', 
                emoji='🍖',
                action=food, 
            ),
            Response(
                'Search for water', 
                emoji='🌊',
                action=water, 
            ),
            Response(
                'Hunt Tributes', 
                emoji='🩸',
                action=lambda: ActionResponse(f'You didn\'t find anyone :/'), 
            ),
        ]
        
        return player.create_prompt(f'What will you do?', responses)

class Snow(Section):
    id = 1
    neighbours = [2, 4]
    thirst = 3
    hunger = 4

class Mountains(Section):
    id = 2
    neighbours = [1, 3, 5]
    thirst = 1
    hunger = 2

class Savanah(Section):
    id = 3
    neighbours = [2, 6]
    thirst = 3
    hunger = 1

class Forest(Section):
    id = 4
    neighbours = [1, 5, 7]
    thirst = 1
    hunger = 2

class Cornucopia(Section):
    id = 5
    neighbours = [2, 4, 8, 6]
    thirst = 2
    hunger = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cornucopia = []

    @property
    def cornucopia(self):
        return [
            m for m in self._cornucopia if m.alive and m in self.players
        ]

    def get_prompt(self, player) -> Prompt:
        if self.game.current_day.date > 1:
           return self.generic_prompt(player)

        def enter():
            resp = ActionResponse(
                f'You enter the Cornucopia. You come across some weapons and food.', 
                public=Message(f'{player.name} bravely enters the Cornucopia.'),
                followup=self.generate_weapon_prompt(player)
            )
            self._cornucopia.append(player)
            return resp

        def run():
            r = random.randint(1, 100)
            if r > 50:
                response = ActionResponse(
                    'You ran away from the cornucopia. What do you do next?', 
                    public=Message(f'{player.name} chooses to run away from the Cornucopia.'),
                    followup=self.generic_prompt(player),
                )
            elif r > 20:
                response = ActionResponse(
                    'You ran away from the cornucopia. On your way you manage to get hold of a bag of weapons.', 
                    public=Message(f'{player.name} chooses to run away from the Cornucopia.'),
                    followup=self.weapon_prompt_run(player),
                )
            elif r > 5: 
                self._cornucopia.append(player)
                followup=None
                if len(self.cornucopia) > 1:
                    followup=self.generate_choose_target_prompt(player)
                player.health -= 15
                response = ActionResponse(
                    "You try to ran away but an arrow hits your leg and you can't run away. You'll need to fight to survive.", 
                    public=Message(f"{player.name} tries to run away but gets injured."),
                    followup=followup
                )
                
            else:
                self.game.kill(player, 'stepped on a landmine')
                response = ActionResponse(
                    'You try to ran away but step on a landmine and die.', 
                    public=Message(f'{player.name} tries to run away but steps on a landmine and dies.'),
                )                  
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
                        followup=self.generate_choose_target_prompt(player),
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
                if player.in_battle:
                    return ActionResponse(
                        f'You are already in a battle!!',
                    )         
                if player.dead:
                    return ActionResponse(
                        f'You are dead!',
                    )                             
                if p.in_battle:
                    return ActionResponse(
                        f'{p} is already in a battle!!',
                        followup=self.generate_choose_target_prompt(player)
                    )              
                if p.dead:
                    return ActionResponse(
                        f'{p} is already dead!',
                        followup=self.generate_choose_target_prompt(player)
                    ) 

                battle = self.game.start_battle(player, p)
                player.finished_responding = True
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
            ) for p in self.cornucopia if p.id != player.id and not p.in_battle
        ]
        return player.create_prompt('Who do you attack?', responses)

    def weapon_prompt_run(self, player):
        def give_weapon(weapon):
            def inner():
                player.weapons.append(weapon)
                return ActionResponse(
                    f'You took the {weapon.name}. What will you do next?', 
                    followup=self.generic_prompt(player),
                )

            return inner

        responses = [
            Response(
                w.name, 
                emoji=w.emoji,
                action=give_weapon(w), 
            ) for w in generate_unique_weapons(3)
        ]

        return player.create_prompt('Which weapon do you pick?', responses)

class Plains(Section):
    id = 6
    neighbours = [3, 5, 9]
    thirst = 1
    hunger = 2

class RainForest(Section):
    id = 7
    neighbours = [4, 8]
    thirst = 1
    hunger = 3

class Grassland(Section):
    id = 8
    neighbours = [5, 7, 9]
    thirst = 2
    hunger = 1

class Desert(Section):
    id = 9
    neighbours = [6, 8]
    thirst = 5
    hunger = 3