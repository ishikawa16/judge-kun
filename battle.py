import random

from constants import WEAPON_LIST


class Battle():
    def __init__(self, team1, team2, player2weapon):
        self.team1 = team1
        self.team2 = team2
        self.player2weapon = player2weapon
        self.winner = None

    def has_player(self, name):
        return name in self.team1 or name in self.team2

    def get_team1(self):
        return self.team1

    def get_team2(self):
        return self.team2

    def get_weapon(self, name):
        return self.player2weapon[name]

    def change_weapon(self, name):
        self.player2weapon[name] = random.choice(WEAPON_LIST)

    def record_winner(self, winner):
        self.winner = winner
