from ....game import Game
from .base import DemonBase


class Imp(DemonBase):
    name = "小恶魔"
    action_guides = "请发送 action@+要猎杀的玩家序号 例如 action@1 ，输入自己序号视为自刀"

    @staticmethod
    def action(targets: list, game: Game):
        player_self = Imp.get_player_self(Imp, game)
        target = targets[0]
        target_player = game.players[target]
        target_player.killed = True
        print(f"玩家 {player_self.name} 猎杀玩家 {target_player.name}")

    @staticmethod
    def dead(game: Game):
        pass
