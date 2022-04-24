import random
from typing import List
from ....player import Player
from .base import MinionBase


class Spy(MinionBase):
    """
    Each night, you see the Grimoire. You might register as good & as a Townsfolk or Outsider, even if dead.
    """
    name = "间谍"

    @property
    def category(self):
        if random.choice([0, 1, 2]):
            from ....TroubleBrewing.role import all_good
            return random.choice(all_good)
        else:
            return Spy

    @staticmethod
    def action(self_player: Player, target_players: List[Player]):
        game = self_player.game()
        other_players = [player for player in game.players if player is not self_player]
        info_list = []
        for player in other_players:
            info = f"玩家 {player.name} 的身份是 {player.role.genuine_category.name}"
            if player.is_drunk:
                info += ",ta是酒鬼"
            if player.is_fake_imp:
                info += ",ta是被占卜师当成恶魔的好人"
            if player.killed:
                info += ",ta是恶魔今晚猎杀的目标"
            if player.poisoned:
                info += ",ta是投毒者今晚下毒的目标"
            info_list.append(info)
        return "\n".join(info_list)
