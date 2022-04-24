from .base import MinionBase


class Poisoner(MinionBase):
    name = "投毒者"
    action_guides = "请发送 action@+要毒的玩家序号,例如 action@3, 发送0则视为不下毒"

    @staticmethod
    def action(self_player, target_players):
        if not target_players:
            return "你没有选择行动目标"
        target_player = target_players[0]
        target_player.poisoned = True
        info = f"玩家 {self_player.name} 对玩家 {target_player.name} 使用毒药"
        print(info)
        return info
