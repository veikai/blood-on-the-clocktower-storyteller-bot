import random
from typing import List
from ....player import Player
from .base import TownsfolkBase


class WasherWoman(TownsfolkBase):
    """
    You start knowing that 1 of 2 players is a particular Townsfolk.
    """
    name = "洗衣妇人"

    @staticmethod
    def action(self_player: Player, target_players: List[Player]):
        game = self_player.game()
        if self_player.poisoned or self_player.is_drunk:
            player1, player2 = random.sample(game.players, 2)
            from ....TroubleBrewing.role import all_townsfolk
            category = random.choice(all_townsfolk)
        else:
            while True:
                player1, player2 = random.sample(game.players, 2)
                if (category := player1.register_as_townsfolk()) or (category := player2.register_as_townsfolk()):
                    break
        return f"玩家 {player1.name} 和 {player2.name} 中有一个 {category.name}"
