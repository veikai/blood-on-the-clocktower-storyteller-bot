import random
from ....game import Game
from .base import TownsfolkBase


class Chef(TownsfolkBase):
    """
    You start knowing how many pairs of evil players there are.
    """
    name = "厨师"

    @staticmethod
    def get_info(game: Game):
        player_self = Chef.get_player_self(Chef, game)
        if player_self.poisoned or player_self.is_drunk:
            if game.players.__len__() <= 9:
                count = random.choice([0, 1])
            elif game.players.__len__() <= 12:
                count = random.choice([0, 1, 2])
            else:
                count = random.choice([0, 1, 2, 3])
        else:
            count = 0
            for i, player in enumerate(game.players):
                if player.is_evil():
                    if i + 1 == game.players.__len__():
                        next_player = game.players[0]
                    else:
                        next_player = game.players[i + 1]
                    if next_player.is_evil():
                        count += 1
        return f"有 {count} 对邻座邪恶玩家"
