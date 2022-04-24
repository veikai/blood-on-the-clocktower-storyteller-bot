import random
from typing import List
from ....player import Player
from .base import TownsfolkBase


class Empath(TownsfolkBase):
    """
    Each night, you learn how many of your 2 alive neighbours are evil.
    """
    name = "共情者"

    @staticmethod
    def action(self_player: Player, target_players: List[Player]):
        game = self_player.game()
        if self_player.is_drunk or self_player.poisoned:
            count = random.choice([0, 1, 2])
        else:
            count = 0
            alive_players = game.alive_players
            if self_player is alive_players[0]:
                previous_player = alive_players[-1]
            else:
                previous_player = alive_players[alive_players.index(self_player) - 1]
            if self_player is alive_players[-1]:
                next_player = alive_players[0]
            else:
                next_player = alive_players[alive_players.index(self_player) + 1]
            if previous_player.register_as_evil():
                count += 1
            if next_player.register_as_evil():
                count += 1
        return f"存活邻座玩家中共有 {count} 个邪恶角色"
