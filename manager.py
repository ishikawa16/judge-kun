from itertools import combinations
import random

from constants import WEAPON_LIST
from player import Player


class Manager:
    """一連の試合の流れを管理
    """
    def __init__(self):
        self.player_db = dict()
        self.alpha = []
        self.bravo = []
        self.team_option = None
        self.weapon_option = None
        self.battle_flag = False

    def add_player(self, name):
        self.player_db[name] = Player()

    def remove_player(self, name):
        del self.player_db[name]

    def has_player(self, name):
        return name in self.player_db

    def get_active_player_db(self):
        return {name: player for name, player in self.player_db.items() if player.is_active()}

    def is_short(self):
        active_player_db = self.get_active_player_db()
        return len(active_player_db) < 2

    def is_over(self):
        active_player_db = self.get_active_player_db()
        return len(active_player_db) > 8

    def start_battle(self):
        self.battle_flag = True

    def finish_battle(self):
        self.battle_flag = False

    def is_during_battle(self):
        return self.battle_flag

    def is_first_battle(self):
        return not self.alpha or not self.bravo

    def rule_determined(self):
        return self.team_option and self.weapon_option

    def set_team_option(self, option):
        self.team_option = option

    def set_weapon_option(self, option):
        self.weapon_option = option

    def display_players(self):
        msg = ""
        msg += "----------Player----------\n"
        for name, player in self.player_db.items():
            if player.is_active():
                msg += f"- __{name}__\n"
            else:
                msg += f"- {name}\n"
        return msg

    def display_ranking(self):
        sorted_players = sorted(
            self.player_db.items(),
            reverse=True,
            key=lambda x: x[1].calculate_wp()
        )

        msg = ""
        msg += "----------Player----------\n"
        for name, player in sorted_players:
            if player.is_rankable():
                wp = player.calculate_wp()
                if player.is_active():
                    msg += f"- __{name}__ ({wp*100:.1f}%)\n"
                else:
                    msg += f"- {name} ({wp*100:.1f}%)\n"
            else:
                if player.is_active():
                    msg += f"- __{name}__ ( - )\n"
                else:
                    msg += f"- {name} ( - )\n"
        return msg

    def display_teams(self):
        msg = ""
        msg += "----------Alpha Team----------\n"
        for name in self.alpha:
            if self.weapon_option == "-a":
                msg += f"- {name}\n"
            else:
                msg += f"- {name} ({self.player_db[name].get_weapon()})\n"
        msg += "----------Bravo Team----------\n"
        for name in self.bravo:
            if self.weapon_option == "-a":
                msg += f"- {name}\n"
            else:
                msg += f"- {name} ({self.player_db[name].get_weapon()})\n"
        return msg

    def display_rule(self):
        option2rule = {"-a": "指定なし", "-f": "固定", "-r": "ランダム", "-w": "勝率", None: " - "}
        msg = ""
        msg += "----------ルール----------\n"
        msg += f"チーム分け:{option2rule[self.team_option]}, 武器:{option2rule[self.weapon_option]}\n"
        return msg

    def split_players(self):
        active_player_db = self.get_active_player_db()
        active_player_names = list(active_player_db.keys())

        if self.team_option == "-w":
            diff = float("inf")
            for comb in combinations(active_player_names, len(active_player_names) // 2):
                alpha_wp, bravo_wp = 0, 0
                for name, player in self.player_db.items():
                    wp = player.calculate_wp()
                    if name in comb:
                        alpha_wp += wp
                    else:
                        bravo_wp += wp

                if abs(alpha_wp - bravo_wp) < diff:
                    diff = abs(alpha_wp - bravo_wp)
                    self.alpha, self.bravo = comb, tuple(set(active_player_names) - set(comb))

        elif self.team_option == "-r":
            comb = random.sample(active_player_names, len(active_player_names) // 2)
            self.alpha, self.bravo = comb, list(set(active_player_names) - set(comb))

    def specify_weapons(self):
        active_player_db = self.get_active_player_db()

        for player in active_player_db.values():
            if self.weapon_option == "-a":
                player.set_weapon(None)
            else:
                player.set_weapon(random.choice(WEAPON_LIST))

    def weapon_specified(self):
        return self.weapon_option == "-r"

    def change_weapon(self, name):
        if self.player_db[name].is_active():
            self.player_db[name].set_weapon(random.choice(WEAPON_LIST))

    def report_alpha_win(self):
        for name in self.alpha:
            self.player_db[name].win()
        for name in self.bravo:
            self.player_db[name].lose()

    def report_bravo_win(self):
        for name in self.alpha:
            self.player_db[name].lose()
        for name in self.bravo:
            self.player_db[name].win()

    def change_status(self, name):
        if self.player_db[name].is_active():
            self.player_db[name].deactivate()
        else:
            self.player_db[name].activate()
