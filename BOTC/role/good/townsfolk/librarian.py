import random
from .base import TownsfolkBase
from ..outsiders import all_outsiders


class Librarian(TownsfolkBase):
    """
    You start knowing that 1 of 2 players is a particular Outsider. (Or that zero are in play.)
    """
    name = "图书管理员"

    @staticmethod
    def get_action_result(self, all_players):
        other_players = [player for player in all_players if player is not self]
        if self.is_drunk or self.is_poisoned:
            if random.choice([True, False]):
                player1, player2 = random.sample(other_players, 2)
                return (f"玩家 {all_players.index(player1)} 和 {all_players.index(player2)} "
                        f"中间有一个外来者 {random.choice(all_outsiders).name}")
            else:
                return "本局游戏没有外来者"
        else:
            outsider_players = []
            player2role = {}
            for player in other_players:
                if role := player.is_outsider():
                    outsider_players.append(player)
                    player2role[player] = role
            if not outsider_players:
                return "本局游戏没有外来者"
            outsider_player = random.choice(outsider_players)
            while True:
                player2 = random.choice(other_players)
                if player2 is not outsider_player:
                    index1, index2 = all_players.index(outsider_player), all_players.index(player2)
                    index_list = [str(index1 + 1), str(index2 + 1)]
                    random.shuffle(index_list)
                    return f"玩家 {'和'.join(index_list)} 中间有一个外来者 {player2role[outsider_player].name}"
