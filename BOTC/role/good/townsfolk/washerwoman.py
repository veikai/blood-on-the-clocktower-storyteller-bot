import random
from .base import TownsfolkBase


class WasherWoman(TownsfolkBase):
    """
    You start knowing that 1 of 2 players is a particular Townsfolk.
    """
    name = "洗衣妇人"

    @staticmethod
    def get_action_result(self, all_players):
        other_players = [player for player in all_players if player is not self]
        if self.is_poisoned or self.is_drunk:
            from ..townsfolk import all_townsfolk
            player1, player2 = random.sample(other_players, 2)
            role = random.choice(all_townsfolk)
        else:
            while True:
                player1, player2 = random.sample(other_players, 2)
                player = random.choice([player1, player2])
                if role := player.is_townsfolk():
                    break
        return f"玩家 {all_players.index(player1) + 1} 和 {all_players.index(player2) + 1} 中间有一个 {role.name}"
