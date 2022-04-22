import random
from .base import OutsiderBase


class Recluse(OutsiderBase):
    name = "隐士"
    fake_role = None

    @staticmethod
    def at_night(all_roles):
        from ...evil.minions import all_minions
        from ...evil.demons import all_demons
        role_type = random.choice([0, 1, 2])
        if role_type == 1:
            Recluse.fake_role = random.choice(all_minions)
        elif role_type == 2:
            Recluse.fake_role = random.choice(all_demons)
        else:
            Recluse.fake_role = Recluse
