class Player:
    def __init__(self):
        self.weapon = None
        self.win_count = 0
        self.match_count = 0

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
