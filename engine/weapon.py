import random

weapons = {
  "Axe": {
    "emoji": "🪓",
    "power": (30, 50),
  },
  "Throwing axe": {
    "emoji": "🪓",
    "power": (40, 50),
  },
  "Bow and arrow": {
    "emoji": "🏹",
    "power": (30, 70),
  },
  "Crossbow": {
    "emoji": "🏹",
    "power": (40, 60),
  },
  "Knife": {
    "emoji": "🔪",
    "power": (20, 50),
  },
  "Throwing knife": {
    "emoji": "🔪",
    "power": (30, 50),
  },
  "Mace": {
    "emoji": "⚔",
    "power": (25, 45),
  },
  "Machete": {
    "emoji": "⚔",
    "power": (30, 45),
  },
  "Spear": {
    "emoji": "🗡",
    "power": (20, 45),
  },
  "Diamond Sword": {
    "emoji": "⚔",
    "power": (35, 70),
  },
  "Trident": {
    "emoji": "🔱",
    "power": (20, 60),
  },
  "Slingshot": {
    "emoji": "✂",
    "power": (30, 50),
  }
}



class Weapon:
    def __init__(self, name, emoji, level, power = None):
        self.name = name
        self.emoji = emoji
        self.level = level
        self.power = power or Weapon.get_power(self.name, 60)

    def upgrade(self):
        self.level += 1
        self.power *= self.level
        self.power += random.randrange(-10, 10)

    @classmethod
    def from_name(cls, name, level=1):
        weapon = weapons[name]
        return Weapon(name, weapon['emoji'], level)

    @classmethod
    def random(cls, level=1):
        weapon = random.choice(list(weapons.keys()))
        return Weapon.from_name(weapon, level)

    @staticmethod
    def get_power(weapon_name, default = None):
        weapon = weapons.get(weapon_name)
        if weapon is None:
            return default
        return random.randint(*weapon['power'])

    def __repr__(self):
        return f'<Weapon {self.name}: Level {self.level} | Power {self.power}>'

    def __str__(self):
        return self.name
        
def generate_unique_weapons(n=1):
    return [
        Weapon.from_name(w) for w in
        random.choices(list(weapons.keys()), k=n)
    ]
