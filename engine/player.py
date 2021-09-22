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