import random
from typing import List
from ....player import Player
from .base import TownsfolkBase


class RavenKeeper(TownsfolkBase):
    """
    If you die at night, you are woken to choose a player: you learn their character.
    """
    name = "守鸦人"

    @staticmethod
    def action(self_player: Player, target_players: List[Player]):
        if not self_player.is_dead:
            return "无信息"
        if not target_players:
            return "你没有选择行动目标"
        target_player = target_players[0]
        if self_player.is_drunk or self_player.poisoned:
            from ....TroubleBrewing.role import all_roles
            role = random.choice([role for role in all_roles if role is not RavenKeeper])
        else:
            if target_player.is_drunk:
                from ....TroubleBrewing.role import Drunk
                role = Drunk
            else:
                role = target_player.role.category
        return f"玩家 {target_player} 的身份是 {role.name}"
