import random
from typing import List
from .evil import all_evil, all_demons, all_minions
from .evil.minions import Baron, ScarletWoman, Spy, Poisoner
from .good import all_good, all_outsiders, all_townsfolk
from .good.outsiders import Drunk
from .evil.demons import Imp
from .good.outsiders import Saint, Butler
from .good.townsfolk import (Virgin, Slayer, Librarian, WasherWoman, Investigator, Chef, RavenKeeper, UnderTaker, Mayor,
                             Monk, Soldier, FortuneTeller, Empath)
from ..player import Player


all_roles = all_evil + all_good
action_order_at_first_night = (Poisoner, WasherWoman, Librarian, Investigator, Chef, Empath, FortuneTeller, Butler, Spy)
action_order_at_night = (Poisoner, Monk, ScarletWoman, Imp, RavenKeeper, Empath, FortuneTeller, Butler, UnderTaker, Spy)

player_role_num = {
    5: (3, 0, 1, 1),
    6: (3, 1, 1, 1),
    7: (5, 0, 1, 1),
    8: (5, 1, 1, 1),
    9: (5, 2, 1, 1),
    10: (7, 0, 2, 1),
    11: (7, 1, 2, 1),
    12: (7, 2, 2, 1),
    13: (9, 0, 3, 1),
    14: (9, 1, 3, 1),
    15: (9, 2, 3, 1)
}


def _generate_game_roles(player_num):
    game_roles = []
    if player_num < 5 or player_num > 15:
        raise Exception("The number of players should be between 5 and 15")
    townsfolk_num, outsider_num, minion_num, demon_num = player_role_num[player_num]
    for demon in random.sample(all_demons, demon_num):
        game_roles.append(demon)
    for minion in random.sample(all_minions, minion_num):
        game_roles.append(minion)
    if Baron in game_roles:
        outsider_num += 2
        townsfolk_num -= 2
    for townsfolk in random.sample(all_townsfolk, townsfolk_num):
        game_roles.append(townsfolk)
    for outsider in random.sample(all_outsiders, outsider_num):
        game_roles.append(outsider)
    random.shuffle(game_roles)
    return game_roles


def assign_roles(players: List[Player]):
    player_num = players.__len__()
    game_roles = _generate_game_roles(player_num)
    evil_players = []
    good_players = []
    for i, role in enumerate(game_roles):
        player = players[i]
        print("玩家", player.name, "的真实身份是", role.name)
        if role is Drunk:
            # 给酒鬼玩家分配村民角色
            other_townsfolk = [role for role in all_townsfolk if role not in game_roles]
            role = random.choice(other_townsfolk)
            player.is_drunk = True
        player.role = role
        if role in all_evil:
            evil_players.append(player)
        else:
            good_players.append(player)
    if FortuneTeller in game_roles:  # 如果存在占卜师，随机一个被占卜师视为恶魔的玩家
        unlucky_players = [player for player in good_players if player is not FortuneTeller]
        random.choice(unlucky_players).is_fake_demon = True
