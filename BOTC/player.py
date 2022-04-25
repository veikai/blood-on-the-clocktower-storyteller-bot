import weakref
import importlib
from flask_socketio import emit


class Player:
    def __init__(self, game, name, sid):
        self.game = weakref.ref(game)
        self.game_module = importlib.import_module(game.__module__)
        self.name = name
        self.sid = sid
        self.role = None
        self.is_dead = False
        self.protected = False  # 夜晚被保护
        self.poisoned = False  # 夜晚被毒
        self.killed = False  # 夜晚被杀
        self.butler = None  # 跟票管家
        self.non_voting = False  # 无投票权
        self.extra_info = ""
        self.__died_of_killing = False  # 夜晚被杀死
        self.__died_of_voting = False  # 被投票处决死
        # for Trouble Brewing
        self.is_drunk = False  # 酒鬼身份
        self.is_fake_imp = False  # 被占卜师当成恶魔的好人

    @property
    def died_of_killing(self):
        return self.__died_of_killing

    @died_of_killing.setter
    def died_of_killing(self, value):
        if value:
            self.is_dead = True
        self.__died_of_killing = value

    @property
    def died_of_voting(self):
        return self.__died_of_voting

    @died_of_voting.setter
    def died_of_voting(self, value):
        if value:
            self.is_dead = True
        self.__died_of_voting = value

    def init(self, game):
        self.game = weakref.ref(game)
        self.game_module = importlib.import_module(game.__module__)
        self.role = None
        self.is_dead = False
        self.protected = False  # 夜晚被保护
        self.poisoned = False  # 夜晚被毒
        self.killed = False  # 夜晚被杀
        self.butler = None  # 跟票管家
        self.non_voting = False  # 无投票权
        self.extra_info = ""
        self.__died_of_killing = False  # 夜晚被杀死
        self.__died_of_voting = False  # 被投票处决死
        # for Trouble Brewing
        self.is_drunk = False  # 酒鬼身份
        self.is_fake_imp = False  # 被占卜师当成恶魔的好人

    def init_night(self):
        self.killed = False
        self.poisoned = False
        self.protected = False
        self.butler = None

    def send_action_guides(self):
        if self.extra_info:
            self.send(self.extra_info)
            self.extra_info = ""
        self.send(self.role.action_guides)

    def action(self, targets: list):
        result = self.role.action(self, targets)
        if result:
            self.send(result)

    def register_as_good(self):
        if (category := self.role.category) in self.game_module.all_good:
            return category
        return None

    def register_as_evil(self):
        if (category := self.role.category) in self.game_module.all_evil:
            return category
        return None

    def register_as_townsfolk(self):
        if (category := self.role.category) in self.game_module.all_townsfolk:
            return category
        return None

    def register_as_outsider(self):
        from .role.good.outsiders import Drunk
        if (category := self.role.category) in self.game_module.all_outsiders:
            return category
        elif self.is_drunk:  # Trouble Brewing
            return Drunk
        return None

    def register_as_minion(self):
        if (category := self.role.category) in self.game_module.all_minions:
            return category
        return None

    def register_as_demon(self):
        from .role.evil.demons import Imp
        if (category := self.role.category) in self.game_module.all_demons:
            return category
        elif self.is_fake_imp:  # Trouble Brewing
            return Imp
        return None

    def is_evil(self):
        if self.role.genuine_category in self.game_module.all_evil:
            return True
        return False

    def is_good(self):
        if self.role.genuine_category in self.game_module.all_good:
            return True
        return False

    def send(self, msg):
        emit("message", msg, room=self.sid)
