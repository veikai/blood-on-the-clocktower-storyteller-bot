import random
from ....game import Game
from ....role import all_roles
from ...good.outsiders import Recluse, Drunk
from ...evil.minions import Spy
from .base import TownsfolkBase


class RavenKeeper(TownsfolkBase):
    """
    If you die at night, you are woken to choose a player: you learn their character.
    """
    name = "守鸦人"
    action_guides = ""
    target = 0

    @staticmethod
    def action(targets: list, game: Game):
        RavenKeeper.target = targets[0]

    @staticmethod
    def get_info(game: Game):
        if not RavenKeeper.target:
            return
        player_self = RavenKeeper.get_player_self(RavenKeeper, game)
        target_player = game.players[RavenKeeper.target]
        if RavenKeeper.target == -1 or RavenKeeper.target == game.players.index(player_self):
            return
        if player_self.is_drunk or player_self.poisoned:
            other_roles = [role for role in all_roles if role is not RavenKeeper]
            role = random.choice(other_roles)
        else:
            if target_player.is_drunk:
                role = Drunk
            elif target_player.role is Spy or target_player.role is Recluse:
                role = target_player.role.fake_role
            else:
                role = target_player.role
        return f"玩家 {target_player} 的身份是 {role.name}"

    @staticmethod
    def dead(game: Game):
        pass

