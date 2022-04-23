import random
from ....game import Game
from .base import TownsfolkBase


class FortuneTeller(TownsfolkBase):
    """
    Each night, choose 2 players: you learn if either is a Demon. There is a good player that registers as a Demon to you.
    """
    name = "占卜师"
    action_guides = "请发送 action@+要查验的两名玩家序号，以英文逗号分隔，例如 action@3,5"
    targets = []

    @staticmethod
    def action(targets, game: Game):
        FortuneTeller.targets = targets

    @staticmethod
    def get_info(game: Game):
        player_self = FortuneTeller.get_player_self(FortuneTeller, game)
        if player_self.is_dead or player_self.is_drunk or player_self.is_poisoned:
            count = random.choice([0, 1, 2])
        else:
            count = 0
            for player_index in FortuneTeller.targets:
                target_player = game.players[player_index]
                if target_player.is_demon():
                    count += 1
        return f"玩家 {' 和 '.join([game.players[index].name for index in FortuneTeller.targets])} 中有 {count} 个恶魔"

