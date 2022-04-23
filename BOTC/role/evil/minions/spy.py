import random
from ....game import Game
from ...good import all_good
from ...good.outsiders import Drunk
from .base import MinionBase


class Spy(MinionBase):
    """
    Each night, you see the Grimoire. You might register as good & as a Townsfolk or Outsider, even if dead.
    """
    name = "间谍"
    fake_role = None

    @staticmethod
    def init_night():
        if random.choice([0, 1, 2]):
            Spy.fake_role = random.choice(all_good)
        else:
            Spy.fake_role = Spy

    @staticmethod
    def get_info(game: Game):
        player_self = Spy.get_player_self(Spy, game)
        other_players = [player for player in game.players if player is not player_self]
        info_list = []
        for player in other_players:
            if player.is_drunk:
                role_name = Drunk.name
            else:
                role_name = player.role.name
            info = f"{player.name} 的身份是 {role_name}"
            if player.is_fake_demon:
                info += ",ta是占卜师的天敌"
            if player.killed:
                info += ",ta是恶魔今晚猎杀的目标"
            if player.poisoned:
                info += ",ta是投毒者今晚下毒的目标"
            info_list.append(info)
        return "\n".join(info_list)
