from .weapon import Weapon
from .prompts import Prompt

import random

class CustomList(list):
    def __repr__(self):
        if not self:
            return 'None'
        return ', '.join([str(i) for i in self])

class Player:
    def __init__(self, name, id):
        self.name = name
        self.id = id

        # Stats
        self.health = 100
        self.hunger = 0
        self.thirst = 0
        self.strength = random.randint(50, 90)

        # Extra
        self.location = None 
        self.weapons: CustomList[Weapon] = CustomList()
        self.killed = CustomList()
        self.reason_of_death = None
        self.hands = Weapon(
            'Fist', '👊', 
            accuracy=90,
            power=random.randint(5, 15)
        )

        # Runtime
        self.responses:int = 0
        self.response = None
        self.prompt = None
        self.finished_responding = False

        self.battle = None
        self.primary_weapon = None # To be set during battles

    @classmethod
    def from_member(cls, member):
        return cls(member.name, member.id)

    @property
    def dead(self) -> bool:
        return any([
            self.health <= 0,
            self.hunger > 100, 
            self.thirst > 100, 
            self.reason_of_death is not None
        ])
    
    @property
    def alive(self) -> bool:
        return not self.dead

    @property
    def responded(self) -> bool:
        return self.responses > 0

    @property
    def in_battle(self) -> bool:
        return self.battle is not None
    
    @property
    def hunger_rate(self) -> int:
        rate = self.strength/100
        return round(rate*self.location.hunger*random.uniform(0.5,1))

    @property
    def thirst_rate(self) -> int:
        rate = self.strength/100
        return round(rate*self.location.thirst*random.uniform(0.75,1.5))

    def update_hunger_and_thirst(self):
        self.hunger += self.hunger_rate
        self.thirst += self.thirst_rate

        #health regen
        if not self.in_battle and self.health < 100:
            self.health += 1

    def __repr__(self):
        return f'<Player: {self.name} {self.id}>'

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def reset_responses(self):
        self.responses = 0
        self.response = None
        self.prompt = None        
        self.finished_responding = False
    
    def add_response(self, response):
        self.responses += 1
        self.response = self.prompt.responses[response]
        return self.response

    def get_prompt(self):
        prompt = self.location.get_prompt(self)
        return self.set_prompt(prompt)

    def set_prompt(self, prompt):
        self.prompt = prompt
        return self.prompt

    def create_prompt(self, *args, **kwargs):
        return self.set_prompt(Prompt(*args, **kwargs))

    def kill(self, reason):
        self.health = 0
        self.reason_of_death = reason

    def get_death_reason(self):
        if not self.reason_of_death:
            if self.hunger > 100:
                self.kill('starved to death')
            elif self.thirst > 100:
                self.kill('died of dehydration')
            elif self.killed_by:
                self.kill(f'got killed by {self.killed_by}')
            elif self.health < 100:
                self.kill('succumbed to their injuries')

        return self.reason_of_death 

    @property
    def usable_weapons(self):
        return self.weapons + [self.hands]

    @property
    def body_parts(self):
        # TODO: OOP smh
        return [
            # name, emoji, size (1-10), vulnerability (1-10)
            ('Head', '👨‍🦱',  4, 8), 
            ('Body', '👕', 10, 4), # large area ->  might not hit an organ
            ('Legs', '👖',  8, 5), # reduces mobility
            ('Feet', '👞',  2, 5) # reduces mobility
        ]
    
    def get_body_part(self, location):
        for part in self.body_parts:
            if location.lower() == part[0].lower():
                return part