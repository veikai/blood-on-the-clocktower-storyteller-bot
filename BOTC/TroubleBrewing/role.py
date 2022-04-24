import random
from typing import List
from ..role.evil.demons import *
from ..role.evil.minions import *
from ..role.good.outsiders import *
from ..role.good.townsfolk import *
from ..player import Player


all_demons = [Imp]
all_minions = [Baron, Poisoner, ScarletWoman, Spy]
all_outsiders = [Butler, Drunk, Recluse, Saint]
all_townsfolk = [Chef, Empath, FortuneTeller, Investigator, Librarian, Mayor, Monk, RavenKeeper, Slayer, Soldier,
                 UnderTaker, Virgin, WasherWoman]
all_evil = all_demons + all_minions
all_good = all_outsiders + all_townsfolk
all_roles = all_evil + all_good
action_order_at_first_night = (Poisoner, WasherWoman, Librarian, Investigator, Chef, Empath, FortuneTeller, Butler, Spy)
action_order_at_night = (Poisoner, Monk, Imp, RavenKeeper, Empath, FortuneTeller, Butler, UnderTaker, Spy)

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
    for i, role in enumerate(game_roles):
        player = players[i]
        print("给玩家", player.name, "分配的身份是", role.name)
        if role is Drunk:
            # 给酒鬼玩家分配村民角色
            role = random.choice([role for role in all_townsfolk if role not in game_roles])
            player.is_drunk = True
        player.role = role()
    if FortuneTeller in game_roles:  # 如果存在占卜师，随机一个被占卜师视为恶魔的玩家
        unlucky_player = random.choice([player for player in players if player.role.genuine_category in all_good])
        unlucky_player.is_fake_imp = True
