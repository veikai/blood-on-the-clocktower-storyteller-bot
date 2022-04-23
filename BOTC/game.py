import random
from enum import Enum
from functools import partial
from typing import List
from .player import Player


class Stage(Enum):
    day = 1
    night = 2
    first_night = 3


class Game:
    def __init__(self):
        self.players: List[Player] = []
        self.stage = Stage.first_night
        self.player2action = {}
        self.action_order = []  # 夜晚玩家行动顺序
        self.dead_cache = []  # 已死亡玩家
        self.nominated_players = {}  # 被提名玩家
        self.vote_cache = []  # 已投票玩家
        self.nominator_cache = []  # 提名他人的玩家

    async def add_player(self, websocket):
        player = Player(self, str(self.players.__len__() + 1), websocket)
        self.players.append(player)
        await self.send_all(f"玩家 {player.name} 加入游戏")

    def new_game(self):
        self.stage = Stage.first_night
        self.player2action.clear()
        self.action_order.clear()
        self.dead_cache.clear()
        self.nominated_players.clear()
        self.vote_cache.clear()
        self.nominator_cache.clear()

    async def night_action(self):
        from .role import action_order_at_first_night, action_order_at_night
        self.action_order = [player for player in self.players if not player.is_dead]
        random.shuffle(self.action_order)
        if self.stage is Stage.first_night:
            role_action_order = action_order_at_first_night
        elif self.stage is Stage.night:
            role_action_order = action_order_at_night
        else:
            raise Exception("game stage error")
        for player in self.action_order:
            if player.role in role_action_order and (action_msg := player.get_action_guides()):
                self.player2action[player] = None
                await player.send(action_msg)
        if not self.player2action:
            await self.process_actions()

    async def start(self):
        self.new_game()
        from .role import assign_roles
        assign_roles(self.players)
        for i, player in enumerate(self.players):
            await player.send(f"你的身份是 {player.role.name}")
        await self.night_action()

    async def do_action(self, player_index: int, target: list):
        player = self.players[player_index]
        if player in self.player2action:
            self.player2action[player] = partial(player.action, target)
            if all(self.player2action.values()):
                print("所有玩家行动决策完毕")
                await self.process_actions()

    async def process_actions(self):
        """
        结算当晚行动并向玩家发送行动结果
        :return:
        """
        from .role import action_order_at_first_night, action_order_at_night
        from .role.good.townsfolk import Soldier, Mayor, RavenKeeper
        from .role.good import all_good
        from .role.evil.demons import Imp
        from .role.evil.minions import all_minions
        self.init_night()
        role2player = {player.role: player for player in self.players if not player.is_dead}
        if self.stage is Stage.first_night:
            action_order = action_order_at_first_night
        elif self.stage is Stage.night:
            action_order = action_order_at_night
        else:
            raise Exception("game stage error")
        for order_role in action_order:
            if order_role in role2player:
                player = role2player[order_role]
                if player in self.player2action:
                    action = self.player2action[player]
                    action()
        for player in self.action_order:
            if player.killed:
                if player.role is Soldier and not player.is_drunk and not player.poisoned and not player.protected:
                    continue
                elif player.role is Mayor and not player.is_drunk and not player.poisoned and not player.protected:
                    # TODO: 替死概率
                    # if not random.choice(range(self.action_order.__len__())):
                    if not random.choice([0, 1, 2]):
                        scapegoats = [player for player in self.action_order if player.role in all_good]
                        scapegoat = random.choice(scapegoats)
                        scapegoat.is_dead = True
                elif not player.protected:
                    player.is_dead = True
        for player in self.action_order:
            await player.send_info()
        await self.next_stage()

    def init_night(self):
        for player in self.players:
            player.init_night()

    async def next_stage(self):
        self.nominated_players.clear()
        self.vote_cache.clear()
        self.nominator_cache.clear()
        if self.stage == Stage.first_night or self.stage == Stage.night:
            self.stage = Stage.day
            await self.send_all("天亮了")
            for player in self.players:
                if player.is_dead and player not in self.dead_cache:
                    await self.send_all(f"今晚死亡的是玩家 {player.name}")
                    break
            else:
                await self.send_all("今晚是平安夜")
            await self.send_all(f"请玩家 {random.choice(self.players).name} 号玩家开始发言")
        elif self.stage == Stage.day:
            self.stage = Stage.night
            self.init_night()
            await self.send_all("天黑了")
            await self.night_action()

    async def nominate(self, nominator_index: int, nominated_index: int):
        """
        提名
        :param nominator_index: 提名他人的玩家索引
        :param nominated_index: 被提名的玩家索引
        :return:
        """
        nominator_player = self.players[nominator_index]  # 提名他人的玩家
        nominated_player = self.players[nominated_index]
        if nominated_player not in self.nominated_players and nominator_player not in self.nominator_cache:
            from .role.good.townsfolk import Virgin, all_townsfolk
            await self.send_all(f"玩家 {nominator_player.name} 提名投票处决 玩家{nominated_player.name}")
            if (nominated_player.role is Virgin
                    and not nominated_player.is_drunk
                    and not nominated_player.poisoned
                    and not nominator_player.is_drunk
                    and nominator_player.role in all_townsfolk):
                # 若真实村民提名了正常状态下的真实圣女 真实村民玩家死亡
                nominator_player.is_dead = True
                await self.send_all(f"玩家 {nominator_player.name} 因提名投票处决 玩家 {nominated_player.name} 死亡")
                await self.next_stage()
            else:
                self.vote_cache.append(nominator_player)
                self.nominator_cache.append(nominator_player)
                self.nominated_players[nominated_player] = [nominator_player]
                if nominated_player.butler:
                    self.nominated_players[nominated_player].append(nominated_player.butler)
        else:
            await nominator_player.send("玩家一天只能提名或被提名一次")

    async def vote(self, index: int, target: int):
        """
        投票
        :param index: 投票玩家索引
        :param target: 被投票玩家索引
        :return:
        """
        vote_player = self.players[index]
        target_player = self.players[target]
        if (not vote_player.non_voting
                and vote_player not in self.vote_cache
                and target_player in self.nominated_players):
            if vote_player.is_dead:
                vote_player.non_voting = True
            self.vote_cache.append(vote_player)
            self.nominated_players[target_player].append(vote_player)
            if vote_player.butler:
                self.nominated_players[target_player].append(vote_player.butler)
            await self.send_all(f"玩家 {vote_player.name} 投票处决 玩家 {target_player.name}")
        else:
            await vote_player.send("无效投票")

    async def execute(self):
        """
        根据投票结果执行处决
        :return:
        """
        if not self.nominated_players:
            return
        from .role.good.outsiders import Saint
        from .role.good.townsfolk import Mayor
        from .role.evil.minions import ScarletWoman
        from .role.evil.demons import Imp
        alive_players = [player for player in self.players if not player.is_dead]
        vote_results = sorted(self.nominated_players.items(), key=lambda item: item[1].__len__(), reverse=True)
        if (vote_results[0][1].__len__() > alive_players.__len__() / 2 and
                vote_results[0][1].__len__() > vote_results[1][1].__len__()):
            # 得票第一多的玩家得票数量超过存活玩家半数且没有平票，执行处决
            executed_player = vote_results[0][0]
            executed_player.is_dead = True
            executed_player.executed_by_vote = True
            await self.send_all(f"玩家 {executed_player.name} 被处决死亡")
            if executed_player.role is Saint and not executed_player.is_poisoned:
                await self.send_all("圣徒被处决死亡，好人失败，游戏结束")
            elif executed_player.role is Imp:
                for player in alive_players:
                    if player.role is ScarletWoman and alive_players.__len__() - 1 >= 5:
                        # 如果小恶魔被处决死亡，且场上存活玩家不少于五人 猩红女郎变成变成恶魔
                        player.extra_info = "因小恶魔被处决死亡，你变身为小恶魔"
                        player.role = Imp
                        break
                else:
                    await self.send_all("恶魔被处决死亡，好人胜利，游戏结束")
            else:
                await self.next_stage()
        else:
            await self.send_all("被提名者得票不过存活玩家数量一半或平票，无人被处决")
            for player in alive_players:
                if (player.role is Mayor
                        and not player.is_drunk
                        and not player.poisoned
                        and alive_players.__len__() == 3):
                    await self.send_all("市长带领好人获得胜利，游戏结束")
                    break

    async def send_all(self, msg):
        for player in self.players:
            await player.send(msg)


game = Game()
