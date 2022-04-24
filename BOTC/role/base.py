from typing import List
from ..player import Player


class RoleBase:
    name = ""
    action_guides = "请发送 action 跳过当前阶段"

    @property
    def genuine_category(self):
        return type(self)

    @property
    def category(self):
        return self.genuine_category

    @staticmethod
    def action(self_player: Player, target_players: List[Player]):
        """
        角色行动逻辑
        :param self_player: 持有角色的玩家
        :param target_players: 行动目标玩家
        :return:
        """
        pass
