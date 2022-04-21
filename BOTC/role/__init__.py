import random
from .evil import all_evils, all_demons, all_minions
from .evil.minions import Baron, ScarletWoman, Spy, Poisoner
from .good import all_good, all_outsiders, all_townsfolk
from .good.outsiders import Drunk
from .evil.demons import Imp
from .good.outsiders import Saint
from .good.townsfolk import Virgin, Slayer, Librarian, WasherWoman, Investigator, Chef, RavenKeeper, UnderTaker, Mayor


all_roles = all_evils + all_good
skip_at_first_night = (UnderTaker, Imp)

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


def assign_roles(player_num):
    game_roles = []
    if player_num < 5 or player_num > 15:
        raise Exception("too many players")
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
        if outsider is Drunk:
            while True:
                fake_role = random.choice(all_townsfolk)
                if fake_role not in game_roles:
                    fake_role.is_drunk = True
                    break
            game_roles.append(fake_role)
            continue
        game_roles.append(outsider)
    random.shuffle(game_roles)
    return game_roles
