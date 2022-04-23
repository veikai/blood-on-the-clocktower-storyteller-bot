import random
from ....game import Game
from .base import TownsfolkBase


class WasherWoman(TownsfolkBase):
    """
    You start knowing that 1 of 2 players is a particular Townsfolk.
    """
    name = "洗衣妇人"

    @staticmethod
    def get_info(game: Game):
        player_self = WasherWoman.get_player_self(WasherWoman, game)
        other_players = [player for player in game.players if player is not player_self]
        if player_self.poisoned or player_self.is_drunk:
            from ..townsfolk import all_townsfolk
            other_townsfolk = [role for role in all_townsfolk if role is not WasherWoman]
            player1, player2 = random.sample(other_players, 2)
            role = random.choice(other_townsfolk)
        else:
            while True:
                player1, player2 = random.sample(other_players, 2)
                if (role := player1.is_townsfolk()) or (role := player2.is_townsfolk()):
                    break
        return f"玩家 {player1.name} 和 {player2.name} 中有一个 {role.name}"
