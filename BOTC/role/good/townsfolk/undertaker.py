import random
from ....game import Game
from ....role import all_roles
from ...good.outsiders import Recluse, Drunk
from ...evil.minions import Spy
from .base import TownsfolkBase


class UnderTaker(TownsfolkBase):
    """
    Each night*, you learn which character died by execution today.
    """
    name = "掘墓人"
    action_guides = "请发送 action@+要挖坟的玩家序号，例如 action@2\n发送0则视为不挖坟"
    target = 0

    @staticmethod
    def action(targets: list, game: Game):
        target = targets[0]
        target_player = game.players[target]
        if target_player.executed_by_vote:
            UnderTaker.target = target

    @staticmethod
    def get_info(game: Game):
        if not UnderTaker.target:
            return
        player_self = UnderTaker.get_player_self(UnderTaker, game)
        target_player = game.players[UnderTaker.target]
        if player_self.is_dead or player_self.is_drunk or player_self.poisoned:
            other_roles = [role for role in all_roles if role is not UnderTaker]
            role = random.choice(other_roles)
        else:
            if target_player.is_drunk:
                role = Drunk
            elif target_player.role is Spy or target_player.role is Recluse:
                role = target_player.role.fake_role
            else:
                role = target_player.role
        return f"玩家 {target_player} 的身份是 {role.name}"
