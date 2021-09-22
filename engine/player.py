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
        self.strength = random.randint(70, 100)

        # Extra
        self.weapons: list[Weapon] = []
        self.killed = []
        self.dead: bool = False
        self.killed_by = None

    @classmethod
    def from_member(cls, member):
        return cls(member.name, member.id)
