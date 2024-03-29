class Player:
    """各プレイヤーの情報を管理
    """
    def __init__(self):
        self.status = True
        self.weapon = None
        self.win_count = 0
        self.match_count = 0

    def is_active(self):
        return self.status

    def activate(self):
        self.status = True

    def deactivate(self):
        self.status = False

    def get_weapon(self):
        return self.weapon

    def set_weapon(self, weapon):
        self.weapon = weapon

    def win(self):
        self.win_count += 1
        self.match_count += 1

    def lose(self):
        self.match_count += 1

    def calculate_wp(self):
        if self.match_count == 0:
            return 0
        return self.win_count / self.match_count

    def is_rankable(self):
        return self.match_count > 0
