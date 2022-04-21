from .base import TownsfolkBase


class FortuneTeller(TownsfolkBase):
    name = "占卜师"
    is_drunk = False

    @staticmethod
    def get_action_msg():
        return "请发送要查验的两名玩家序号"
