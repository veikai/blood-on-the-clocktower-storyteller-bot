from typing import List
from ..game import Game


class RoleBase:
    name = ""
    action_guides = ""

    @staticmethod
    def init_night():
        pass

    @staticmethod
    def action(targets: List[int], game: Game):
        """
        :param targets: 目标玩家索引
        :param game: 游戏上下文
        :return:
        """
        pass

    @staticmethod
    def get_info(game: Game):
        """
        获取夜晚信息或行动结果
        :param game: 游戏上下文
        :return:
        """
        pass

    @staticmethod
    def get_player_self(cls, game: Game):
        alive_players = [player for player in game.players if not player.is_dead]
        for player in alive_players:
            if player.role is cls:
                return player

    @staticmethod
    def dead(game: Game):
        """
        死亡触发事件
        :param game:
        :return:
        """
        pass
