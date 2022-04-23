from ....game import Game
from .base import OutsiderBase


class Butler(OutsiderBase):
    name = "管家"
    action_guides = "请发送 action@+要跟票的玩家序号，例如 action@2\n发送0则视为不跟票"

    @staticmethod
    def action(targets: list, game: Game):
        player_self = Butler.get_player_self(Butler, game)
        target = targets[0]
        if target == -1 or target == game.players.index(player_self):
            return
        target_player = game.players[target]
        target_player.butler = player_self
        print(f"玩家 {player_self.name} 跟票玩家 {target_player.name}")
