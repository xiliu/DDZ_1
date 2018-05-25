# coding: utf-8

from Card import *
import operator
import random
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Poker:
    def __init__(self,card_count=54):

        '''
        参数：
            card_count：牌的张数，默认54张（目前只考虑斗地主的情况）
        '''

        if card_count == 54:
            self.card_count = card_count
        else:
            logger.error("初始牌数出错，card_count = "+str(card_count))
            return
        self.cards = []
        for i in range(52):
            card = Card((i%13)+1,int(i/13)+1)
            self.cards.append(card)
        card_l_king = Card(14, 5)
        card_b_king = Card(15, 5)
        self.cards.append(card_l_king)
        self.cards.append(card_b_king)

    #洗牌
    def shuffle(self):
        for i in range(self.card_count*3):
            n1 = int(random.uniform(0, self.card_count))
            n2 = int(random.uniform(0, self.card_count))

            card_tmp = self.cards[n1]
            self.cards[n1] = self.cards[n2]
            self.cards[n2] = card_tmp

    #发牌
    def deal(self):
        for card in self.cards:
            if operator.eq(card.status,'暗牌'):
                card.set_status('手牌')
                return card
        logger.warning("没有底牌可发了...")
        return None

    def detail(self):
        for i in range(self.card_count):
            self.cards[i].detail()