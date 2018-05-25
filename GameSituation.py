# coding: utf-8
#游戏全局类,当前游戏的发展情况

class GameSituation:
    def __init__(self,players,dipai_cards):
        self.players = players         #本局3名玩家
        self.dizhu_id = -1             #本局地主id
        self.land_score = 0            #本局地主叫分
        self.dipai_cards = dipai_cards #三张底牌
        self.contrller_id = -1         #当前控手玩家，（用于区分是否可以自身任意出牌以及是否地主已经放弃出牌从而不去管队友）
        self.is_game_over = False      #游戏是否结束