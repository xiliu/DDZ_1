# coding: utf-8

import operator
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Card:
    def __init__(self,card_value,card_type,status="暗牌"):
        '''
        参数:
            card_value: 牌的点数，14为小王，15为大王
            card_type: 牌的花色，1-梅花、2-黑桃、3-方片、4-红桃、5-大小王
            status: 牌所处的状态，分别为：暗牌（荷官手中的牌，所有玩家不知道内容）、手牌（玩家手中的牌，只有所持有该牌的玩家知道内容）、
                    明牌（被打出的牌,所有玩家都知道牌的内容）、底牌（3张地主加的牌）
        '''

        card_value = int(card_value)

        if card_value<1 or card_value>15:
            logger.error("初始牌点数出错，card_value = " + str(card_value))
            return

        if operator.eq(card_type,'梅花'):
            card_type = 1
        elif operator.eq(card_type,'黑桃'):
            card_type = 2
        elif operator.eq(card_type,'方片'):
            card_type = 3
        elif operator.eq(card_type,'红桃'):
            card_type = 4
        elif operator.eq(card_type,'大王'):
            card_type = 5
        elif operator.eq(card_type,'小王'):
            card_type = 5
        else:
            card_type = int(card_type)

        if card_type<1 or card_type>5:
            logger.error("初始牌花色出错，card_type = "+str(card_type))
            return
        else:
            if card_type == 5:
                if card_value<14:
                    logger.error("初始牌花色或点数出错，card_type = " + str(card_type)+"  card_value=" + str(card_value))
                    return
                else:
                    self.card_type = card_type
                    self.card_value = card_value
            else:
                if card_value>13:
                    logger.error("初始牌花色或点数出错，card_type = " + str(card_type)+"  card_value=" + str(card_value))
                    return
                else:
                    self.card_type = card_type
                    self.card_value = card_value

        self.status = status

    def set_status(self,status):
        status_ann = ['暗牌','手牌','明牌','底牌']
        if status in status_ann:
            self.status = status
        else:
            logger.warning("设置牌的状态不在规定范围内..")

    def detail(self):
        if self.card_type == 1:
            if self.card_value == 11:
                print("♣J",end=" ")
            elif self.card_value == 12:
                print("♣Q",end=" ")
            elif self.card_value == 13:
                print("♣K",end=" ")
            elif self.card_value == 1:
                print("♣A", end=" ")
            else:
                print("♣"+str(self.card_value),end=" ")
        elif self.card_type == 2:
            if self.card_value == 11:
                print("♠J",end=" ")
            elif self.card_value == 12:
                print("♠Q",end=" ")
            elif self.card_value == 13:
                print("♠K",end=" ")
            elif self.card_value == 1:
                print("♠A", end=" ")
            else:
                print("♠"+str(self.card_value),end=" ")
        elif self.card_type == 3:
            if self.card_value == 11:
                print("♦J",end=" ")
            elif self.card_value == 12:
                print("♦Q",end=" ")
            elif self.card_value == 13:
                print("♦K",end=" ")
            elif self.card_value == 1:
                print("♦A", end=" ")
            else:
                print("♦"+str(self.card_value),end=" ")
        elif self.card_type == 4:
            if self.card_value == 11:
                print("♥J",end=" ")
            elif self.card_value == 12:
                print("♥Q",end=" ")
            elif self.card_value == 13:
                print("♥K",end=" ")
            elif self.card_value == 1:
                print("♥A", end=" ")
            else:
                print("♥"+str(self.card_value),end=" ")
        elif self.card_type == 5:
            if self.card_value == 14:
                print("小王",end=" ")
            elif self.card_value == 15:
                print("大王",end=" ")
            else:
                logger.error("点数不合法，card_value = " + str(self.card_value)+"  card_type = "+ str(self.card_type))
        else:
            logger.error("花色不合法，card_type = " + str(self.card_type))