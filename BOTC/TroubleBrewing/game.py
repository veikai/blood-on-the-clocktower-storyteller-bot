import random
from enum import Enum
from typing import List
from ..player import Player
from .role import (all_demons, all_minions, all_outsiders, all_townsfolk, all_evil, all_good, all_roles, assign_roles,
                   action_order_at_first_night, action_order_at_night, Virgin, Saint, Imp, ScarletWoman, Mayor, Slayer)


class Stage(Enum):
    day = 1
    night = 2
    first_night = 3


class Game:
    def __init__(self):
        self.players: List[Player] = []
        self.stage = Stage.first_night
        self.player2action = {}
        self.action_players = []  # 夜晚玩家行动顺序
        self.action_order = ()
        self.nominated_players = {}  # 被提名玩家
        self.vote_cache = []  # 已投票玩家
        self.nominator_cache = []  # 提名他人的玩家
        self.shoot_cache = []
        self.dead_players = []
        self.action_player = None  # 当前行动玩家

    @property
    def alive_players(self):
        return [player for player in self.players if not player.is_dead]

    # @property
    # def dead_players(self):
    #     return [player for player in self.players if player.is_dead]

    @property
    def evil_players(self):
        return [player for player in self.players if player.role.genuine_category in all_evil]

    async def add_player(self, websocket):
        player = Player(self, str(self.players.__len__() + 1), websocket)
        self.players.append(player)
        await self.send_all(f"玩家 {player.name} 加入游戏")

    def new_game(self):
        self.stage = Stage.first_night
        self.player2action.clear()
        self.action_players.clear()
        self.nominated_players.clear()
        self.vote_cache.clear()
        self.nominator_cache.clear()
        self.shoot_cache.clear()
        self.dead_players.clear()
        for player in self.players:
            player.init(self)

    async def night_action(self):
        if self.stage is Stage.first_night:
            self.action_order = action_order_at_first_night
        elif self.stage is Stage.night:
            self.action_order = action_order_at_night
        else:
            raise Exception("game stage error")
        for category in self.action_order:
            for player in self.alive_players:
                if player.role.genuine_category is category:
                    self.action_players.append(player)
                    break
        non_action_players = [player for player in self.alive_players if player not in self.action_players]
        while non_action_players:
            player = non_action_players.pop()
            if self.action_players:
                index = random.choice(range(self.action_players.__len__()))
                self.action_players.insert(index, player)
            else:
                self.action_players.append(player)
        self.action_players.reverse()
        while self.action_players:
            self.action_player = self.action_players.pop()
            print(self.action_player.name, "轮次")
            if self.stage is Stage.first_night and self.action_player in self.evil_players:
                evil_partners = [player for player in self.evil_players if player is not self.action_player]
                partner_info = "\n".join([f'玩家 {player.name}, ta的身份是 {player.role.genuine_category.name}'
                                          for player in evil_partners])
                await self.action_player.send(f"你的伙伴是：\n{partner_info}")
            if self.action_player.role.genuine_category in self.action_order:
                await self.action_player.send_action_guides()
                break
        else:
            await self.next_stage()

    async def start(self):
        self.new_game()
        assign_roles(self.players)
        for i, player in enumerate(self.players):
            await player.send(("发送 action@玩家序号 选择行动目标，多个目标用英文逗号分隔，例如 action2 action3,5\n"
                               "发送 nominate@玩家序号 提名投票处决目标玩家 例如 nominate@2\n"
                               "发送 vote@玩家序号 投票处决目标玩家 例如 vote@2\n"
                               "发送 shoot@玩家序号 对目标玩家开枪 例如 shoot@2"))
            await player.send(f"你的身份是 {player.role.name}")
        await self.night_action()

    async def do_action(self, player_index: int, targets: list):
        player = self.players[player_index]
        if player is self.action_player:
            await player.action(targets)
        while self.action_players:
            self.action_player = self.action_players.pop()
            print(self.action_player.name, "轮次")
            if self.stage is Stage.first_night and self.action_player in self.evil_players:
                evil_partners = [player for player in self.evil_players if player is not self.action_player]
                partner_info = "\n".join([f'玩家 {player.name}, ta的身份是 {player.role.genuine_category.name}'
                                          for player in evil_partners])
                await self.action_player.send(f"你的伙伴是：\n{partner_info}")
            if self.action_player.role.genuine_category in self.action_order:
                await self.action_player.send_action_guides()
                break
        else:
            await self.next_stage()

    def init_night(self):
        for player in self.players:
            player.init_night()

    async def next_stage(self):
        self.nominated_players.clear()
        self.vote_cache.clear()
        self.nominator_cache.clear()
        self.shoot_cache.clear()
        if self.stage == Stage.first_night or self.stage == Stage.night:
            self.stage = Stage.day
            await self.send_all("天亮了")
            dead_at_night = []
            for player in self.players:
                if player.is_dead and player not in self.dead_players:
                    self.dead_players.append(player)
                    dead_at_night.append(player)
            if dead_at_night:
                await self.send_all(f"今晚死亡的是 {','.join([f'玩家 {player.name}' for player in dead_at_night])}")
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
        nominated_player = self.players[nominated_index]  # 被提名玩家
        if nominated_player not in self.nominated_players and nominator_player not in self.nominator_cache:
            await self.send_all(f"玩家 {nominator_player.name} 提名投票处决 玩家{nominated_player.name}")
            if (nominated_player.role.genuine_category is Virgin
                    and not nominated_player.is_drunk
                    and not nominated_player.poisoned
                    and not nominator_player.is_drunk
                    and nominator_player.role.genuine_category in all_townsfolk):
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
        alive_players = self.alive_players
        vote_results = sorted(self.nominated_players.items(), key=lambda item: item[1].__len__(), reverse=True)
        do_execution = False
        if vote_results[0][1].__len__() > alive_players.__len__() / 2:
            do_execution = True
            if vote_results.__len__() > 1 and vote_results[0][1].__len__() == vote_results[1][1].__len__():
                do_execution = False
        if do_execution:
            # 得票第一多的玩家得票数量超过存活玩家半数且没有平票，执行处决
            executed_player = vote_results[0][0]
            executed_player.is_dead = True
            executed_player.executed_by_vote = True
            await self.send_all(f"玩家 {executed_player.name} 被处决死亡")
            if executed_player.role.genuine_category is Saint and not executed_player.is_poisoned:
                await self.send_all("圣徒被处决死亡，好人失败，游戏结束")
            elif executed_player.role.genuine_category is Imp:
                for player in alive_players:
                    if player.role.genuine_category is ScarletWoman and self.alive_players.__len__() >= 5:
                        # 如果小恶魔被处决死亡，且场上存活玩家不少于五人 猩红女郎变成变成恶魔
                        player.extra_info = "因小恶魔被处决死亡，你变身为小恶魔"
                        player.role = Imp()
                        break
                else:
                    await self.send_all("恶魔被处决死亡，好人胜利，游戏结束")
            else:
                alive_players = self.alive_players
                evil_player = [player for player in alive_players if player.is_evil()]
                good_player = [player for player in alive_players if player.is_good()]
                if evil_player.__len__() >= good_player.__len__():
                    await self.send_all("邪恶玩家人数>=好人人数，好人失败，游戏结束")
                else:
                    await self.next_stage()
        else:
            await self.send_all("被提名者得票不过存活玩家数量一半或平票，无人被处决")
            for player in alive_players:
                if (player.role.genuine_category is Mayor
                        and not player.is_drunk
                        and not player.poisoned
                        and alive_players.__len__() == 3):
                    await self.send_all("市长带领好人获得胜利，游戏结束")
                    break

    async def shoot(self, index: int, target: int):
        shoot_player = self.players[index]
        target_player = self.players[target]
        if shoot_player not in self.shoot_cache:
            self.shoot_cache.append(shoot_player)
            if (shoot_player.role.category is Slayer
                    and not shoot_player.is_drunk
                    and not shoot_player.poisoned
                    and target_player.register_as_demon()):
                await self.send_all(f"玩家 {shoot_player.name} 开枪打死了玩家 {target_player.name}")
            else:
                await self.send_all(f"玩家 {shoot_player.name} 对玩家 {target_player.name} 开了一枪，但无事发生")
        else:
            await shoot_player.send("一天只能开一枪")

    async def send_all(self, msg):
        for player in self.players:
            await player.send(msg)


game = Game()
