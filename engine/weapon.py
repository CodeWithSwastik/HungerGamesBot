import random

weapons = {
  "Axe": {
    "emoji": "🪓",
    "power": (30, 50),
    "accuracy": 65,
  },
  "Throwing axe": {
    "emoji": "🪓",
    "power": (40, 50),
    "accuracy": 40,
  },
  "Blowgun": {
    "emoji": "🌬",
    "power": (20, 40),
    "accuracy": 65,
  },
  "Bow and arrow": {
    "emoji": "🏹",
    "power": (30, 70),
    "accuracy": 75,
  },
  "Crossbow": {
    "emoji": "🏹",
    "power": (40, 60),
    "accuracy": 85,
  },
  "Knife": {
    "emoji": "🔪",
    "power": (20, 50),
    "accuracy": 80,
  },
  "Throwing knife": {
    "emoji": "🔪",
    "power": (30, 50),
    "accuracy": 55,
  },
  "Mace": {
    "emoji": "⚔",
    "power": (25, 45),
    "accuracy": 70,
  },
  "Machete": {
    "emoji": "⚔",
    "power": (30, 45),
    "accuracy": 75,
  },
  "Spear": {
    "emoji": "🗡",
    "power": (20, 45),
    "accuracy": 65,
  },
  "Diamond Sword": {
    "emoji": "⚔",
    "power": (35, 70),
    "accuracy": 80,
  },
  "Trident": {
    "emoji": "🔱",
    "power": (20, 60),
    "accuracy": 70,
  },
  "Slingshot": {
    "emoji": "✂",
    "power": (30, 50),
    "accuracy": 65,
  },
  "Your mom": {
    "emoji": "👧",
    "power": (80, 90),
    "accuracy": 10,
  }
}



class Weapon:
    def __init__(self, name, emoji, level=1, accuracy = None, power = None):
        self.name = name
        self.emoji = emoji
        self.level = level
        self.accuracy = accuracy or Weapon.get_accuracy(self.name, 60) # 0-100%
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

    @staticmethod
    def get_accuracy(weapon_name, default = None):
        weapon = weapons.get(weapon_name)
        if weapon is None:
            return default
        return weapon['accuracy']

    def __repr__(self):
        return f'<Weapon {self.name}: Level {self.level} | Power {self.power}>'

    def __str__(self):
        return self.name

def generate_unique_weapons(n=1):
    return [
        Weapon.from_name(w) for w in
        random.choices(list(weapons.keys()), k=n)
    ]
