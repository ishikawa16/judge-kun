class Rule:
    """試合のルール内容を保持
    """
    OPTION2CAPTION = {"-a": "指定なし", "-f": "固定", "-r": "ランダム", "-w": "勝率", None: " - "}

    def __init__(self):
        self.team_option = None
        self.weapon_option = None

    def display(self):
        msg = ""
        msg += "----------ルール----------\n"
        msg += f"チーム分け:{self.OPTION2CAPTION[self.team_option]}, 武器:{self.OPTION2CAPTION[self.weapon_option]}\n"
        return msg

    def is_determined(self):
        return self.team_option is not None and self.weapon_option is not None

    def get_team_option(self):
        return self.team_option

    def get_weapon_option(self):
        return self.weapon_option

    def set_team_option(self, option):
        self.team_option = option

    def set_weapon_option(self, option):
        self.weapon_option = option
