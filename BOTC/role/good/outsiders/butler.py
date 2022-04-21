from .base import OutsiderBase


class Butler(OutsiderBase):
    name = "管家"

    @staticmethod
    def get_action_msg():
        return "请发送要跟票的玩家序号，发送0则视为不跟票"

    @staticmethod
    def action(target: list, all_players: list):
        target = target[0]
        if target >= all_players.__len__():
            return
        all_players[target].with_butler = True
