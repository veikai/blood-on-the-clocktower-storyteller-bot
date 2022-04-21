import random
from .base import OutsiderBase


class Recluse(OutsiderBase):
    name = "隐士"

    @property
    def is_evil(self):
        return random.choice([0, 1, 2]) != 2

    @property
    def is_demon(self):
        return random.choice([0, 1, 2]) == 0
