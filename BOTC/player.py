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

    @property
    def id_dead(self):
        if not self.__is_dead:
            self.__is_dead = self.killed and not self.protected
            self.killed = False
            self.protected = False
        return self.__is_dead

    def action(self):
        pass

    async def send(self, msg):
        await self.websocket.send(msg)
