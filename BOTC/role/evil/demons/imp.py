import random
from typing import List
from ....player import Player
from ...good.townsfolk import Soldier, RavenKeeper
from .base import DemonBase


class Imp(DemonBase):
    name = "小恶魔"
    action_guides = "请发送 action@+要猎杀的玩家序号 例如 action@1 ，输入自己序号视为自刀"

    @staticmethod
    def action(self_player: Player, target_players: List[Player]):
        if not target_players:
            return "你没有选择行动目标"
        target_player = target_players[0]
        target_player.killed = True
        info = f"玩家 {self_player.name} 猎杀玩家 {target_player.name}"
        print(info)
        if not target_player.protected:
            if target_player.role.category is Soldier and not target_player.is_drunk and not target_player.poisoned:
                return info
            elif target_player.role.category is RavenKeeper:
                target_player.role.category.action_guides = "你在今晚被杀死，请发送 action@+要查看身份的玩家序号，例如 action@2"
            elif target_player is self_player:
                # 小恶魔自刀 随机一个爪牙变成小恶魔
                game = self_player.game()
                if lucky_dogs := [player for player in game.alive_players if player.register_as_minion()]:
                    lucky_dog = random.choice(lucky_dogs)
                    lucky_dog.role = Imp()
                    lucky_dog.extra_info = "因小恶魔选择自刀，你成为了小恶魔"
                else:
                    game = self_player.game()
                    game.send_all("小恶魔自刀且没有能够变成小恶魔的爪牙，好人胜利，游戏结束")
            target_player.died_of_killing = True
        return info
