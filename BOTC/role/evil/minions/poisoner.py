from .base import MinionBase


class Poisoner(MinionBase):
    name = "投毒者"

    @staticmethod
    def get_action_msg():
        return "请发送要毒的玩家序号"

    @staticmethod
    def action(target: list, all_players: list):
        target = target[0]
        if target >= all_players.__len__():
            return
        all_players[target].is_poisoned = True
        print(f"投毒者给 {target} 号玩家下毒")
