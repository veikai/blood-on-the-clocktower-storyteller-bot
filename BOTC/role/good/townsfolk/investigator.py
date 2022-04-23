import random
from ....game import Game
from .base import TownsfolkBase


class Investigator(TownsfolkBase):
    """
    You start knowing that 1 of 2 players is a particular Minion.
    """
    name = "调查者"

    @staticmethod
    def get_info(game: Game):
        player_self = Investigator.get_player_self(Investigator, game)
        other_players = [player for player in game.players if player is not player_self]
        if player_self.poisoned or player_self.is_drunk:
            from ...evil.minions import all_minions
            player1, player2 = random.sample(other_players, 2)
            role = random.choice(all_minions)
        else:
            while True:
                player1, player2 = random.sample(other_players, 2)
                if (role := player1.is_minion()) or (role := player2.is_minion()):
                    break
        return f"玩家 {player1.name} 和 {player2.name} 中有一个 {role.name}"
