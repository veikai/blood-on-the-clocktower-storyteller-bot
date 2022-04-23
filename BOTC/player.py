import random
import weakref


class Player:
    def __init__(self, game, name, websocket):
        self.game = weakref.ref(game)
        self.name = name
        self.websocket = websocket
        self.role = None
        self.__is_dead = False
        self.killed = False  # 夜晚被杀
        self.protected = False  # 夜晚被保护
        self.poisoned = False  # 夜晚被毒
        self.butler = None  # 跟票管家
        self.is_fake_demon = False  # 被占卜师视为恶魔
        self.is_drunk = False  # 酒鬼
        self.non_voting = False  # 无投票权
        self.extra_info = ""
        self.executed_by_vote = False

    @property
    def is_dead(self):
        return self.__is_dead

    @is_dead.setter
    def is_dead(self, value):
        self.__is_dead = value
        if value:
            self.role.dead()

    def init_night(self):
        self.poisoned = False
        self.protected = False
        self.killed = False
        self.butler = None
        self.role.init_night()

    def get_action_guides(self):
        return self.role.action_guides

    def action(self, targets: list):
        return self.role.action(targets, self.game())

    def is_evil(self):
        from .role.evil import all_evil
        from .role.evil.minions import Spy
        from .role.good.outsiders import Recluse
        if self.role in all_evil:
            return True
        elif self.role is Recluse and Recluse.fake_role in all_evil:
            return True
        elif self.role is Spy and Spy.fake_role in all_evil:
            return True
        return False

    def is_townsfolk(self):
        from .role.good import all_townsfolk
        from .role.evil.minions import Spy
        if self.role in all_townsfolk:
            return self.role
        elif self.role is Spy and Spy.fake_role in all_townsfolk:
            return self.role.fake_role
        return None

    def is_outsider(self):
        from .role.good import all_outsiders
        from .role.evil.minions import Spy
        from .role.good.outsiders import Drunk
        if self.role in all_outsiders:
            return self.role
        elif self.role is Spy and Spy.fake_role in all_outsiders:
            return self.role.fake_role
        elif self.is_drunk:
            return Drunk
        return None

    def is_minion(self):
        from .role.evil import all_minions
        from .role.good.outsiders import Recluse
        from .role.evil.minions import Spy
        if self.role is Spy and Spy.fake_role in all_minions:
            return self.role
        elif self.role in all_minions:
            return self.role
        elif self.role is Recluse and Recluse.fake_role in all_minions:
            return self.role.fake_role
        return None

    def is_demon(self):
        from .role.evil import all_demons
        from .role.good.outsiders import Recluse
        if self.role in all_demons:
            return self.role
        elif self.role is Recluse and Recluse.fake_role in all_demons:
            return self.role.fake_role
        elif self.is_fake_demon:
            return random.choice(all_demons)
        return None

    async def send_info(self):
        if self.extra_info:
            await self.send(self.extra_info)
            self.extra_info = ""
        info = self.role.get_info(self.game())
        if info:
            await self.send(info)

    async def send(self, msg):
        await self.websocket.send(msg)
