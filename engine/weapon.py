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
  "Sickle": {
    "emoji": "🪓",
    "power": (50, 65),
    "accuracy": 55,
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
  }
}



class Weapon:
    def __init__(self, name, emoji, accuracy = None, power = None):
        self.name = name
        self.emoji = emoji
        self.accuracy = accuracy or Weapon.get_accuracy(self.name, 60) # 0-100%
        self.power = power or Weapon.get_power(self.name, 60)

    @classmethod
    def from_name(cls, name):
        weapon = weapons[name]
        return Weapon(name, weapon['emoji'])

    @classmethod
    def random(cls):
        weapon = random.choice(list(weapons.keys()))
        return Weapon.from_name(weapon)

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
        return f'<Weapon {self.name}: Power {self.power}>'

    def __str__(self):
        return self.name

def generate_unique_weapons(n=1):
    e = list(weapons.keys())
    random.shuffle(e)
    return [
        Weapon.from_name(w) for w in
        e[:n]
    ]