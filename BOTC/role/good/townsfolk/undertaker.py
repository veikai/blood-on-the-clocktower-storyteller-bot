import random
from typing import List
from ....player import Player
from .base import TownsfolkBase


class UnderTaker(TownsfolkBase):
    """
    Each night*, you learn which character died by execution today.
    """
    name = "掘墓人"
    action_guides = "请发送 action@+要挖坟的玩家序号，例如 action@2\n发送0则视为不挖坟"

    @staticmethod
    def action(self_player: Player, target_players: List[Player]):
        target_player = target_players[0]
        if not target_player.died_of_voting:
            self_player.send("只能挖被投票处决的坟")
            return
        if self_player.is_dead or self_player.is_drunk or self_player.poisoned:
            from ....TroubleBrewing.role import all_roles
            role = random.choice([role for role in all_roles if role is not UnderTaker])
        else:
            if target_player.is_drunk:
                from ....TroubleBrewing.role import Drunk
                role = Drunk
            else:
                role = target_player.role.category
        return f"玩家 {target_player} 的身份是 {role.name}"
