import random
from typing import List
from ....player import Player
from .base import TownsfolkBase


class Librarian(TownsfolkBase):
    """
    You start knowing that 1 of 2 players is a particular Outsider. (Or that zero are in play.)
    """
    name = "图书管理员"

    @staticmethod
    def action(self_player: Player, target_players: List[Player]):
        game = self_player.game()
        if self_player.is_drunk or self_player.poisoned:
            if random.choice([True, False]):
                player1, player2 = random.sample(game.players, 2)
                from ....TroubleBrewing.role import all_outsiders
                info = f"玩家 {player1.name} 和 {player2.name} 中有一个 {random.choice(all_outsiders).name}"
            else:
                info = "本局游戏没有外来者"
        else:
            outsider_players = [(player, category) for player in game.players
                                if (category := player.register_as_outsider())]
            if not outsider_players:
                info = "本局游戏没有外来者"
            else:
                player1, category = random.choice(outsider_players)
                while True:
                    player2 = random.choice(game.players)
                    if player2 is not player1:
                        player_list = [player1.name, player2.name]
                        random.shuffle(player_list)
                        info = f"玩家 {'和'.join(player_list)} 中有一个 {category.name}"
                        break
        return info
