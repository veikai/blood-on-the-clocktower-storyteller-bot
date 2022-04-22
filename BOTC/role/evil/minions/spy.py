import random
from ...good import all_good
from .base import MinionBase


class Spy(MinionBase):
    """
    Each night, you see the Grimoire. You might register as good & as a Townsfolk or Outsider, even if dead.
    """
    name = "间谍"
    fake_role = None

    @staticmethod
    def at_night(all_roles):
        if random.choice([0, 1, 2]):
            Spy.fake_role = random.choice(all_good)
        else:
            Spy.fake_role = Spy

