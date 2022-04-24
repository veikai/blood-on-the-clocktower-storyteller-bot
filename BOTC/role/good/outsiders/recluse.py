import random
from .base import OutsiderBase


class Recluse(OutsiderBase):
    name = "隐士"
    fake_role = None

    @property
    def category(self):
        from ....TroubleBrewing.role import Imp, all_minions
        role_type = random.choice([0, 1, 2])
        if role_type == 1:
            return random.choice(all_minions)
        elif role_type == 2:
            return Imp
        else:
            return Recluse
