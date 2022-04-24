from typing import List
from ....player import Player
from .base import OutsiderBase


class Butler(OutsiderBase):
    name = "管家"
    action_guides = "请发送 action@+要跟票的玩家序号，例如 action@2\n发送0则视为不跟票"

    @staticmethod
    def action(self_player: Player, target_players: List[Player]):
        if not target_players:
            return "你没有选择行动目标"
        target_player = target_players[0]
        if not self_player.poisoned and not self_player.is_dead:
            target_player.butler = self_player
        info = f"玩家 {self_player.name} 跟票玩家 {target_player.name}"
        print(info)
        return info
