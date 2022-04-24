import random
from typing import List
from ....player import Player
from .base import TownsfolkBase


class Investigator(TownsfolkBase):
    """
    You start knowing that 1 of 2 players is a particular Minion.
    """
    name = "调查者"

    @staticmethod
    def action(self_player: Player, target_players: List[Player]):
        game = self_player.game()
        if self_player.poisoned or self_player.is_drunk:
            player1, player2 = random.sample(game.players, 2)
            from ....TroubleBrewing.role import all_minions
            category = random.choice(all_minions)
        else:
            while True:
                player1, player2 = random.sample(game.players, 2)
                if (category := player1.register_as_minion()) or (category := player2.register_as_minion()):
                    break
        return f"玩家 {player1.name} 和 {player2.name} 中有一个 {category.name}"
