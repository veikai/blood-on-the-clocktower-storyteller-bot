import random
from .base import DemonBase
from ..minions import all_minions


class Imp(DemonBase):
    name = "小恶魔"

    @staticmethod
    def get_action_msg():
        return "请发送要猎杀的玩家序号，输入自己序号视为自刀"

    @staticmethod
    def action(target, all_players):
        target = target[0]
        if target >= all_players.__len__():
            return
        target_player = all_players[target]
        all_players[target].killed = True
        if target_player.role is Imp:
            minion_players = [player for player in all_players if player.role in all_minions]
            minion_player = random.choice(minion_players)
            minion_player.role = Imp
        else:
            print("小恶魔猎杀了", target, "号玩家")
