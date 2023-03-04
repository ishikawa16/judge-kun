from collections import deque
import copy
from itertools import combinations
import random

from battle import Battle
from constants import WEAPON_LIST
from player import Player
from rule import Rule


class Manager:
    """一連の試合の流れを管理
    """
    def __init__(self):
        self.player_db = dict()
        self.battle_db = deque()
        self.battle = Battle()
        self.rule = Rule()

    # プレイヤー関連の操作
    def get_player(self, name):
        return self.player_db[name]

    def has_player(self, name):
        return name in self.player_db

    def add_player(self, name):
        self.player_db[name] = Player()

    def remove_player(self, name):
        del self.player_db[name]

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
        sorted_player_db = sorted(
            self.player_db.items(),
            reverse=True,
            key=lambda x: x[1].get_wp()
        )

        msg = ""
        msg += "----------Player----------\n"
        for name, player in sorted_player_db:
            if player.is_rankable():
                wp = player.get_wp()
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

    def get_active_players(self):
        return [name for name, player in self.player_db.items() if player.is_active()]

    def split_players(self, names):
        team_option = self.rule.get_team_option()
        if team_option == "-w":
            diff = float("inf")
            for comb in combinations(names, len(names) // 2):
                team1_wp, team2_wp = 0, 0
                for name, player in self.player_db.items():
                    wp = player.get_wp()
                    if name in comb:
                        team1_wp += wp
                    else:
                        team2_wp += wp

                if abs(team1_wp - team2_wp) < diff:
                    diff = abs(team1_wp - team2_wp)
                    team1, team2 = comb, tuple(set(names) - set(comb))

        elif team_option == "-r":
            comb = random.sample(names, len(names) // 2)
            team1, team2 = comb, list(set(names) - set(comb))

        else:
            battle = self.battle_db[-1]
            team1, team2 = battle.get_team1(), battle.get_team2()
            if set(names) != set(team1 + team2):
                return False

        self.battle.set_team1(team1)
        self.battle.set_team2(team2)
        return True

    def is_short(self):
        active_players = self.get_active_players()
        return len(active_players) < 2

    def is_over(self):
        active_players = self.get_active_players()
        return len(active_players) > 8

    # バトル関連の操作
    def get_battle(self):
        return self.battle

    def get_latest_battle(self):
        if len(self.battle_db) == 0:
            return None
        else:
            return self.battle_db[-1]

    def prepare_battle(self):
        active_players = self.get_active_players()
        if self.split_players(active_players):
            self.specify_weapons(active_players)
            return True
        else:
            return False

    def record_battle(self, winner):
        self.battle.record_winner(winner)
        self.calculate_wp(winner)

        latest_battle = copy.deepcopy(self.battle)
        self.battle_db.append(latest_battle)
        self.battle.reset()

    def specify_weapons(self, names):
        weapon_option = self.rule.get_weapon_option()
        player2weapon = dict()
        for name in names:
            if weapon_option == "-a":
                player2weapon[name] = None
            else:
                player2weapon[name] = random.choice(WEAPON_LIST)
        self.battle.set_player2weapon(player2weapon)

    def calculate_wp(self, winner):
        team1 = self.battle.get_team1()
        team2 = self.battle.get_team2()

        if winner == 1:
            for name in team1:
                self.player_db[name].win()
            for name in team2:
                self.player_db[name].lose()

        else:
            for name in team1:
                self.player_db[name].lose()
            for name in team2:
                self.player_db[name].win()

    def display_teams(self):
        team1 = self.battle.get_team1()
        team2 = self.battle.get_team2()
        weapon_option = self.rule.get_weapon_option()

        msg = ""
        msg += "----------Team1----------\n"
        for name in team1:
            if weapon_option == "-a":
                msg += f"- {name}\n"
            else:
                msg += f"- {name} ({self.battle.get_weapon(name)})\n"
        msg += "----------Team2----------\n"
        for name in team2:
            if weapon_option == "-a":
                msg += f"- {name}\n"
            else:
                msg += f"- {name} ({self.battle.get_weapon(name)})\n"
        return msg

    # ルール関連の操作
    def get_rule(self):
        return self.rule
