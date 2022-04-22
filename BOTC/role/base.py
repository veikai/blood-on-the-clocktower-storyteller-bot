from typing import List
from ..player import Player


class RoleBase:
    is_drunk = False

    @staticmethod
    def get_action_msg():
        pass

    @staticmethod
    def action(target: List[int], all_players: List[Player]):
        pass

    @staticmethod
    def random_action(target: List[int], all_players: List[Player]):
        pass

    @staticmethod
    def get_action_result(self: Player, all_players: List[Player]):
        pass

    @staticmethod
    def at_night(all_roles):
        pass

    @staticmethod
    def at_day():
        pass
