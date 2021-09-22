import random
import json

with open("./engine/data/weapons.json", "r") as f:
    weapons = json.load(f)

for weapon, power in weapons.items():
    weapons[weapon] = random.randrange(power[0], power[1])


class Weapon:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.power = weapons[self.name]

    def upgrade(self):
        self.level += 1
        self.power *= self.level
        self.power += random.randrange(-10, 10)