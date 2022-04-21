import random
from .base import TownsfolkBase
from ..outsiders.base import OutsiderBase
from ..outsiders import Drunk, all_outsiders


class Librarian(TownsfolkBase):
    name = "图书管理员"
    is_drunk = False

    @staticmethod
    def action(target: list, all_players: list):
        if Librarian.is_drunk:
            return Librarian.random_action(target, all_players)
        else:
            outsider_players = [player for player in all_players if issubclass(player.role, OutsiderBase) or player.role.is_drunk]
            if not outsider_players:
                return "本场游戏没有外来者"
            else:
                outsider_player = random.choice(outsider_players)
                outsider_name = Drunk.name if outsider_player.role.is_drunk else outsider_player.role.name
                index1 = all_players.index(outsider_player)
                while True:
                    player = random.choice(all_players)
                    index2 = all_players.index(player)
                    if index1 != index2:
                        index_list = [str(index1), str(index2)]
                        random.shuffle(index_list)
                        return f"玩家 {'和'.join(index_list)} 之间有一个外来者 {outsider_name}"

    @staticmethod
    def random_action(target: list, all_players: list):
        if random.choice([True, False]):
            index_list = [str(all_players.index(player)) for player in random.sample(all_players, 2)]
            return f"玩家 {'和'.join(index_list)} 之间有一个外来者 {random.choice(all_outsiders).name}"
        else:
            return "本场游戏没有外来者"

