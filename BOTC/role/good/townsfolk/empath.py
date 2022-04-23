import random
from ....game import Game
from .base import TownsfolkBase


class Empath(TownsfolkBase):
    """
    Each night, you learn how many of your 2 alive neighbours are evil.
    """
    name = "共情者"

    @staticmethod
    def get_info(game: Game):
        player_self = Empath.get_player_self(Empath, game)
        if player_self.is_drunk or player_self.poisoned:
            count = random.choice([0, 1, 2])
        else:
            count = 0
            alive_players = [player for player in game.players if not player.is_dead]
            self_index = alive_players.index(player_self)
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
