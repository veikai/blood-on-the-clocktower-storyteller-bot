from ....game import Game
from .base import MinionBase


class Poisoner(MinionBase):
    name = "投毒者"
    action_guides = "请发送 action@+要毒的玩家序号,例如 action@3, 发送0则视为不下毒"

    @staticmethod
    def action(targets: list, game: Game):
        player_self = Poisoner.get_player_self(Poisoner, game)
        target = targets[0]
        target_player = game.players[target]
        target_player.poisoned = True
        print(f"玩家 {player_self.name} 对玩家 {target_player.name} 使用毒药")
