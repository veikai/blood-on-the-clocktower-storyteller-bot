import random
from .base import TownsfolkBase


class Chef(TownsfolkBase):
    """
    You start knowing how many pairs of evil players there are.
    """
    name = "厨师"

    @staticmethod
    def get_action_result(self, all_players):
        if self.is_poisoned or self.is_drunk:
            if all_players.__len__() <= 9:
                count = random.choice([0, 1])
            elif all_players.__len__() <= 12:
                count = random.choice([0, 1, 2])
            else:
                count = random.choice([0, 1, 2, 3])
        else:
            count = 0
            for i, player in enumerate(all_players[:-1]):
                if player.is_evil():
                    next_player = all_players[i + 1]
                    if next_player.is_evil():
                        count += 1
        return f"有 {count} 对邻座邪恶玩家"
