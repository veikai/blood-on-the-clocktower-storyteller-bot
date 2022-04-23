from ....game import Game
from .base import TownsfolkBase


class Monk(TownsfolkBase):
    """
    Each night*, choose a player (not yourself): they are safe from the Demon tonight.
    """
    name = "僧侣"
    action_guides = "请发送 action@+要守护的玩家序号,例如 action@3，发送0则视为不守护任何玩家"

    @staticmethod
    def action(targets: list, game: Game):
        player_self = Monk.get_player_self(Monk, game)
        target = targets[0]
        if target == -1 or target == game.players.index(player_self) or player_self.is_drunk or player_self.poisoned:
            return
        target_player = game.players[target]
        target_player.protected = True
        print(f"玩家 {player_self.name} 守护玩家 {target_player.name}")
