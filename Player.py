# coding: utf-8

import itertools
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Player:
    def __init__(self,identifier,cards):
        '''
        参数：
            identifier：玩家标识符、编号
            cards：手牌
        '''
        if identifier in [1,2,3]:
            self.identifier = identifier
        else:
            logger.warning('初始化玩家编号不符合规定...编号为：'+str(identifier))

        if len(cards)  ==17:
            self.__hand_cards = cards          #手牌
            self.hand_cards_count = len(cards) #手牌数
            self.played_cards = []             #已经打出去的牌
            self.played_cards_count = 0        #已经打出去的牌数
        else:
            logger.warning('初始化'+str(identifier)+'号玩家手牌不符合规定...')

        self.hand_card_value = -100 #手牌总价值
        self.need_round = 100       #需要打几手牌

    def get_hand_cards(self):
        return self.__hand_cards

    #整理牌
    def order_cards(self):
        cards_tmp = sorted(self.__hand_cards, key=lambda card: card.card_value)

        #将A和2单独拿出
        cards_A2_tmp = []
        for card in cards_tmp:
            if card.card_value<3:
                cards_A2_tmp.append(card)
        for card in cards_A2_tmp:
            cards_tmp.remove(card)

        #获取将A和2插入序列的位置
        insert_index = 0
        for card in cards_tmp:
            if card.card_value<14:
                insert_index+=1

        #将A和插入牌序列
        for card in cards_A2_tmp:
            cards_tmp.insert(insert_index,card)
            insert_index+=1

        self.__hand_cards = cards_tmp

    #抢地主
    def apply_landlord(self):
        logger.info("抢地主")

    #主动出牌
    def initiative_play_cards(self):
        logger.info("主动出牌")

    #被动出牌
    def passively_play_cards(self):
        logger.info("被动出牌")


    def detail(self):
        print(str(self.identifier)+'号玩家：')
        print('  手牌有'+str(self.hand_cards_count)+"张：",end='')
        for card in self.__hand_cards:
            card.detail()
        print("")
        print('  打出去的牌有' + str(self.played_cards_count) + "张：", end='')
        for card in self.played_cards:
            card.detail()
        print("")


from enum import IntEnum
class CardGroupType(IntEnum):
    cg_ERROR = -1                 #错误类型
    cg_SINGLE = 1                 #单牌类型
    cg_DOUBLE = 2                 #对牌类型
    cg_THREE = 3                  #三条类型
    cg_SINGLE_LINE = 4            #单连类型
    cg_DOUBLE_LINE = 5            #对连类型
    cg_THREE_LINE = 6             #三连类型（飞机不带）
    cg_THREE_TAKE_ONE = 7         #三带一单
    cg_THREE_TAKE_TWO = 8         #三带一对
    cg_AIRCRAFT_SINGLE_CARD = 9   #飞机带单牌
    cg_AIRCRAFT_DOUBLE_CARD = 10  #飞机带对子
    cg_FOUR_TAKE_ONE = 11         #四带两单
    cg_FOUR_TAKE_TWO = 12         #四带两对
    cg_BOMB_CARD = 13             #炸弹类型
    cg_KING_CARD = 14             #王炸类型





class CardsGroupAndValue:

    def __init__(self,cards):
        if len(cards)>0 and len(cards)<21:
            self.cards = cards
        else:
            logger.warning("要计算牌价值的排数不在范围内...")

        self.group_list = []
        self.total_value= -100






