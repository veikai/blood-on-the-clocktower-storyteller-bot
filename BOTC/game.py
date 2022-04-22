import random
from enum import Enum
from threading import Condition
from .player import Player
from .role import assign_roles, skip_at_first_night, get_drunk_role, skip_at_night
from .role.evil.base import EvilBase
from .role.good.outsiders import Drunk


class Stage(Enum):
    day = 1
    night = 2
    first_night = 3


class Game:
    def __init__(self):
        self.players = []
        self.roles = []
        self.stage = Stage.first_night
        self.stage_condition = Condition()
        self.action_condition = Condition()
        self.current_action_index = None
        self.action_order = []

    async def add_player(self, websocket):
        self.players.append(Player(websocket))
        for player in self.players:
            await player.send(f"玩家 {self.players.__len__()} 加入游戏")

    async def start(self):
        evil_player_index = []
        self.roles = assign_roles(self.players.__len__())
        for i, player in enumerate(self.players):
            role = self.roles[i]
            print(f"玩家{i}的角色是", role.name)
            if issubclass(role, EvilBase):
                evil_player_index.append(i)
            if role is Drunk:
                role = get_drunk_role(self.roles)
                player.is_drunk = True
            player.role = role
            await player.send(f"你的身份是 {role.name}")
        for index in evil_player_index:
            player = self.players[index]
            evil_partners = [(i, self.roles[i]) for i in evil_player_index if index != i]
            await player.send(f"你的同伙是")
            for i, role in evil_partners:
                await player.send(f"{i + 1} 号玩家 身份 {role.name}")
        self.action_order = self.players.copy()
        random.shuffle(self.action_order)
        while self.action_order:
            player = self.action_order.pop()
            if player.role in skip_at_first_night:
                continue
            action_msg = player.get_action_msg()
            if action_msg:
                await player.send(action_msg)
            else:
                await self.next_action()
            break
        else:
            await self.send_action_result()

    async def next_action(self):
        if self.action_order:
            player = self.action_order.pop()
            if self.stage == Stage.first_night and player.role in skip_at_first_night:
                await self.next_action()
            elif self.stage == Stage.night and player.role in skip_at_night:
                await self.next_action()
            else:
                action_msg = player.get_action_msg()
                if action_msg:
                    await player.send(action_msg)
                else:
                    await self.next_action()
        else:
            await self.send_action_result()

    async def do_action(self, player_index, target: list):
        player = self.players[player_index]
        player.action(target, self.players)
        await self.next_action()

    async def send_action_result(self):
        for player in self.players:
            result_msg = player.get_action_result(self.players)
            print(player.role.name, "得到的信息是", result_msg)
            if result_msg:
                await player.send(result_msg)

    def nominate(self):
        # 提名
        pass

    def vote(self):
        # 投票
        pass

    def execute(self):
        # 处决
        pass

game = Game()
