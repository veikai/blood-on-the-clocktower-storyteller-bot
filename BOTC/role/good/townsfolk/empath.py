import random
from .base import TownsfolkBase


class Empath(TownsfolkBase):
    name = "共情者"
    is_drunk = False

    @staticmethod
    def get_action_result(self, all_players):
        if self.is_drunk or self.is_poisoned:
            count = random.choice([0, 1, 2])
        else:
            count = 0
            alive_players = [player for player in all_players if not player.is_dead]
            self_index = alive_players.index(self)
            if self_index == 0:
                right_player = alive_players[-1]
            else:
                right_player = alive_players[self_index - 1]
            if self_index == alive_players.__len__() - 1:
                left_player = alive_players[0]
            else:
                left_player = alive_players[self_index + 1]
            if right_player.is_evil():
                count += 1
            if left_player.is_evil():
                count += 1
        return f"存活邻座玩家中共有 {count} 个邪恶角色"
