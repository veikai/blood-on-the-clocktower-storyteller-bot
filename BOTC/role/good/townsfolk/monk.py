from typing import List
from ....player import Player
from .base import TownsfolkBase


class Monk(TownsfolkBase):
    """
    Each night*, choose a player (not yourself): they are safe from the Demon tonight.
    """
    name = "僧侣"
    action_guides = "请发送 action@+要守护的玩家序号,例如 action@3，发送0则视为不守护任何玩家"

    @staticmethod
    def action(self_player: Player, target_players: List[Player]):
        if not target_players:
            return "你没有选择行动目标"
        target_player = target_players[0]
        if target_player is self_player:
            self_player.send("你在想peach")
        else:
            print(f"玩家 {self_player.name} 守护玩家 {target_player.name}")
            if not self_player.is_dead and not self_player.is_drunk and not self_player.poisoned:
                target_player.protected = True
