import random
from ....game import Game
from .base import TownsfolkBase
from ..outsiders import all_outsiders


class Librarian(TownsfolkBase):
    """
    You start knowing that 1 of 2 players is a particular Outsider. (Or that zero are in play.)
    """
    name = "图书管理员"

    @staticmethod
    def get_info(game: Game):
        player_self = Librarian.get_player_self(Librarian, game)
        other_players = [player for player in game.players if player is not player_self]
        if player_self.is_drunk or player_self.poisoned:
            if random.choice([True, False]):
                player1, player2 = random.sample(other_players, 2)
                return f"玩家 {player1.name} 和 {player2.name} 中有一个 {random.choice(all_outsiders).name}"
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
                    player_list = [outsider_player.name, player2.name]
                    random.shuffle(player_list)
                    return f"玩家 {'和'.join(player_list)} 中有一个 {player2role[outsider_player].name}"
