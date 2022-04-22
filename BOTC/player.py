class Player:
    def __init__(self, websocket):
        self.websocket = websocket
        self.role = None
        self.__is_dead = False
        self.killed = False  # 夜晚被杀
        self.protected = False  # 夜晚被保护
        self.is_poisoned = False  # 夜晚被毒
        self.with_butler = False  # 管家跟票
        self.is_fake_demon = False  # 被占卜师视为恶魔
        self.is_drunk = False  # 酒鬼

    @property
    def id_dead(self):
        if not self.__is_dead:
            self.__is_dead = self.killed and not self.protected
            self.killed = False
            self.protected = False
        return self.__is_dead

    def get_action_msg(self):
        return self.role.get_action_msg()

    def action(self, target: list, all_players):
        return self.role.action(target, all_players)

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
        return None

    def get_action_result(self, all_players: list):
        return self.role.get_action_result(self, all_players)

    async def send(self, msg):
        await self.websocket.send(msg)
