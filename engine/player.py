from .weapon import Weapon
import random

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
        self.weapons: list[Weapon] = []
        self.killed = []
        self.killed_by = None

        # Runtime
        self.responses:int = 0
        self.response = None
        self.prompt = None

    @classmethod
    def from_member(cls, member):
        return cls(member.name, member.id)

    @property
    def dead(self) -> bool:
        return any([
            self.health <= 0,
            self.hunger > 100, 
            self.thirst > 100, 
            self.killed_by is not None
        ])

    @property
    def responded(self) -> bool:
        return self.responses > 0
    
    def reset_responses(self):
        self.responses = 0
        self.response = None
        self.prompt = None        
    
    def add_response(self, response):
        self.responses += 1
        self.response = response

    def get_prompt(self):
        self.prompt = self.location.get_prompt(self)
        return self.prompt
