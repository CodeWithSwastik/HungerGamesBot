import random

class Battle:
    def __init__(self, game, player1, player2):
        self.game = game
        self.player1 = player1
        self.player2 = player2
        self.participants = [self.player1.id, self.player2.id]
        self.player1.battle = self
        self.player2.battle = self

        self.over = False
        self.winner = None

    def base_damage(self, player):
        return (player.strength + player.primary_weapon.power)/100


    def get_other(self, player):
        return self.player1 if self.player2 == player else self.player2

    def miss(self, weapon, body_part_size):
        return (weapon.accuracy/100) * (body_part_size/10) > random.random()

    def attack(self, player, location):
        other = self.get_other(player)
        location = player.get_body_part(location)
        if self.miss(other.primary_weapon, location[-2]):
            return None

        mult = location[-1] * random.uniform(2, 3)

        damage = round(self.base_damage(other) * mult)
        player.health -= damage
        if player.dead:
            self.game.kill(player, f'was slain in battle by {other}')
            player.killed_by = other
            other.killed.append(player)

            self.winner = other
            self.end()
        return damage

    def end(self):
        self.over = True
        self.player1.primary_weapon = None
        self.player2.primary_weapon = None
        self.player1.battle = None
        self.player2.battle = None