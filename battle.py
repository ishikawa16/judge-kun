import random

from constants import WEAPON_LIST


class Battle():
    def __init__(self):
        self.team1 = None
        self.team2 = None
        self.player2weapon = None
        self.winner = None

    def is_prepared(self):
        return self.team1 is not None and self.team2 is not None and self.player2weapon is not None

    def has_player(self, name):
        return name in self.team1 or name in self.team2

    def get_team1(self):
        return self.team1

    def get_team2(self):
        return self.team2

    def get_weapon(self, name):
        return self.player2weapon[name]

    def set_team1(self, team1):
        self.team1 = team1

    def set_team2(self, team2):
        self.team2 = team2

    def set_player2weapon(self, player2weapon):
        self.player2weapon = player2weapon

    def change_weapon(self, name):
        self.player2weapon[name] = random.choice(WEAPON_LIST)

    def record_winner(self, winner):
        self.winner = winner

    def reset(self):
        self.team1 = None
        self.team2 = None
        self.player2weapon = None
        self.winner = None
