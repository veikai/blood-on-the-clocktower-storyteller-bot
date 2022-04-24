import random
from typing import List
from ....player import Player
from .base import TownsfolkBase


class FortuneTeller(TownsfolkBase):
    """
    Each night, choose 2 players: you learn if either is a Demon.
    There is a good player that registers as a Demon to you.
    """
    name = "占卜师"
    action_guides = "请发送 action@+要查验的两名玩家序号，以英文逗号分隔，例如 action@3,5"

    @staticmethod
    def action(self_player: Player, target_players: List[Player]):
        if self_player.is_dead or self_player.is_drunk or self_player.poisoned:
            count = random.choice([0, 1, 2])
        else:
            count = [player for player in target_players if player.register_as_demon()].__len__()
        return f"玩家 {' 和 '.join([player.name for player in target_players])} 中有 {count} 个恶魔"

