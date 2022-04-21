from .base import TownsfolkBase


class Monk(TownsfolkBase):
    name = "僧侣"
    is_drunk = False

    @staticmethod
    def get_action_msg():
        return "请发送要守护的玩家序号，发送0则视为不守护任何玩家"
