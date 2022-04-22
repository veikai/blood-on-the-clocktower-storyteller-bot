import random
from enum import Enum
from threading import Condition
from .player import Player
from .role import assign_roles, skip_at_first_night, get_drunk_role, skip_at_night
from .role.evil.base import EvilBase
from .role.good.outsiders import Drunk, Saint
from .role.good.townsfolk import Virgin, all_townsfolk, Mayor
from .role.evil.demons import Imp
from .role.evil.minions import ScarletWoman


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
        self.dead_cache = []
        self.nominated_players = {}
        self.vote_cache = []
        self.nominate_cache = []

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
        self.at_night()
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
            if result_msg:
                print(player.role.name, "得到的信息是", result_msg)
                await player.send(result_msg)

    async def next_stage(self):
        self.nominated_players.clear()
        self.vote_cache.clear()
        self.nominate_cache.clear()
        if self.stage == Stage.first_night or self.stage == Stage.night:
            self.stage = Stage.day
            await self.send_all("天亮了")
            for player in self.players:
                if player.is_dead and player not in self.dead_cache:
                    await self.send_all(f"今晚死亡的是 {self.players.index(player) + 1} 号玩家")
                    break
            else:
                await self.send_all("今晚是平安夜")
            await self.send_all(f"请 {random.choice(range(self.players.__len__()))} 号玩家开始发言")
        elif self.stage == Stage.day:
            self.stage = Stage.night
            self.at_night()
            await self.send_all("天黑了")
            self.action_order = [player for player in self.players if not player.is_dead]
            random.shuffle(self.action_order)
            while self.action_order:
                player = self.action_order.pop()
                if player.role in skip_at_night:
                    continue
                action_msg = player.get_action_msg()
                if action_msg:
                    await player.send(action_msg)
                else:
                    await self.next_action()
                break
            else:
                await self.send_action_result()

    def at_night(self):
        for player in self.players:
            player.at_night(self.roles)

    async def nominate(self, index: int, target: int):
        # 提名
        nominator_player = self.players[index]
        if target not in self.nominated_players and index not in self.nominate_cache:
            await self.send_all(f"{index + 1} 号玩家提名投票处决 {target + 1} 号玩家, 提名自动视为投票")
            target_player = self.players[target]
            if target_player.role is Virgin and not target_player.is_drunk:
                if not nominator_player.is_drunk and nominator_player.role in all_townsfolk:
                    nominator_player.is_dead = True
                    await self.send_all(f"{index + 1} 号玩家死亡")
                    await self.next_stage()
            else:
                self.vote_cache.append(index)
                self.nominate_cache.append(index)
                self.nominated_players[target] = [index + 1]
        else:
            await nominator_player.send("玩家一天只能提名或被提名一次")

    async def vote(self, index: int, target: int):
        # 投票
        player = self.players[index]
        if not player.non_voting:
            if index not in self.vote_cache:
                if target not in self.nominated_players:
                    nominated_players = [str(value) for value in self.nominated_players.values()]
                    await player.send(f"只能给被提名的玩家投票，现在被提名的玩家有：{','.join(nominated_players)}")
                else:
                    if player.is_dead:
                        player.non_voting = True
                    self.vote_cache.append(index)
                    self.nominated_players[target].append(index + 1)
                    if butler_index := player.with_butler:
                        self.nominated_players[target].append(butler_index + 1)
                    await self.send_all(f"{index + 1} 号玩家投票处决 {target + 1} 号玩家")
            else:
                player = self.players[index]
                await player.send("一天只能投票一次 请勿重复投票")
        else:
            await player.send("无投票权")

    async def execute(self):
        # 处决
        alive_players = [player for player in self.players if not player.is_dead]
        if self.nominated_players:
            vote_results = sorted(self.nominated_players.items(), key=lambda item: item[1].__len__(), reverse=True)
            if (vote_results[0][1].__len__() > alive_players.__len__() / 2 and
                    vote_results[0][1].__len__() > vote_results[1][1].__len__()):
                executed_player = self.players[vote_results[0][0]]
                executed_player.is_dead = True
                await self.send_all(f"{vote_results[0][0] + 1} 号玩家被处决死亡")
                if executed_player.role is Saint and not executed_player.is_poisoned:
                    await self.send_all("圣徒被处决死亡，好人失败，游戏结束")
                elif executed_player.role is Imp:
                    for player in alive_players:
                        if player.role is ScarletWoman and alive_players.__len__() - 1 >= 5:
                            # 如果小恶魔被处决死亡，且场上存活玩家不少于五人 猩红女郎变成变成恶魔
                            player.role = Imp
                            break
                    else:
                        await self.send_all("恶魔被处决死亡，好人胜利，游戏结束")
                else:
                    await self.next_stage()
            else:
                await self.send_all("被提名者得票不过存活玩家数量一半或平票，无人被处决")
                for player in alive_players:
                    if (player.role is Mayor and not player.is_drunk and
                            not player.is_poisoned and alive_players.__len__() == 3):
                        await self.send_all("市长带领好人获得胜利，游戏结束")
                        break

    async def send_all(self, msg):
        for player in self.players:
            await player.send(msg)


game = Game()
