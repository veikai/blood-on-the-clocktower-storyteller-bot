import random
from .base import OutsiderBase


class Recluse(OutsiderBase):
    name = "隐士"
    fake_role = None

    @property
    def category(self):
        from ...evil.minions import all_minions
        from ...evil.demons import all_demons
        role_type = random.choice([0, 1, 2])
        if role_type == 1:
            return random.choice(all_minions)
        elif role_type == 2:
            return random.choice(all_demons)
        else:
            return Recluse
