# coding: utf-8

import itertools
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Group:
    def __init__(self,cards):
        self.group_cards = cards    #组合牌序列
        self.group_type = -1        #组合牌型
        #要做归一化TODO
        self.defense_value = -1     #*该组合牌防守价值，通过被动出牌打出去的值（为0时，该组合牌最小，不可能通过被动出牌打出去的，越大越好）
        self.attack_value = -1      #*该组合牌攻击价值，该组合牌打出去被'吃掉'的值（为0时，对手没有大于该组合的牌，越小越好）

    def detail(self):
        for card in self.group_cards:
            card.detail()

    # 判断是否为'单连'类型4
    def is_sigle_line(self):
        n = len(self.group_cards)
        for i in range(n-1):
            if self.group_cards[i].card_value+1 != self.group_cards[i + 1].card_value:
                return False
        if self.group_cards[0].card_value + n - 1 != self.group_cards[-1].card_value:
            return False
        if self.group_cards[0].card_value<3:
            return False
        if self.group_cards[-1].card_value>13:
            return False
        else:
            return True

    #判断是否为'对连'类型5
    def is_double_line(self):
        if len(self.group_cards)%2 == 0:
            n = int(len(self.group_cards)/2)
            for i in range(n):
                if self.group_cards[i*2].card_value != self.group_cards[i*2+1].card_value:
                    return False
                elif self.group_cards[i*2].card_value<3 or self.group_cards[i*2].card_value>13:
                    return False
            if self.group_cards[0].card_value + n -1 != self.group_cards[-1].card_value:
                return False
            else:
                return True
        else:
            return False

    # 判断是否为'三连'类型（飞机不带）6
    def is_three_line(self):
        if len(self.group_cards)%3 == 0:
            n = int(len(self.group_cards)/3)
            for i in range(n):
                if self.group_cards[i*3].card_value != self.group_cards[i*3+2].card_value:
                    return False
                elif self.group_cards[i*3].card_value<3 or self.group_cards[i*3].card_value>13:
                    return False
            if self.group_cards[0].card_value + n -1 != self.group_cards[-1].card_value:
                return False
            else:
                return True
        else:
            return False

    # 判断是否为飞机带单牌7
    def is_aircraft_single_card(self):
        if len(self.group_cards) % 4 == 0:
            n = int(len(self.group_cards) / 4)
            flag = 0
            index = []#找出三条类型的下标

            for i in range(len(self.group_cards)-1):
                if self.group_cards[i].card_value == self.group_cards[i+1].card_value:
                    flag += 1
                else:
                    flag = 0
                if flag == 2:
                    index.append(i)
                    flag = 0
            if len(index) == n:
                for index_i in range(len(index)-1):
                    if self.group_cards[index[index_i]].card_value+1 != self.group_cards[index[index_i+1]].card_value:
                        return False
                    elif self.group_cards[index[index_i]].card_value <3:
                        return False
                return True
            else:
                return False
        else:
            return False

    # 判断是否为飞机带对子8
    def is_aircraft_double_card(self):
        if len(self.group_cards) % 5 == 0:
            n = int(len(self.group_cards) / 5)
            flag = 0
            index_t = []  # 三条类型的下标
            index_d = []  # 对子的下标

            #找出三条类型的下标
            for i in range(len(self.group_cards) - 1):
                if self.group_cards[i].card_value == self.group_cards[i+1].card_value:
                    flag += 1
                else:
                    flag = 0
                if flag == 2:
                    index_t.append(i)
                    flag = 0
            # 找出对子类型的下标
            for i in range(len(self.group_cards) - 1):
                if self.group_cards[i].card_value == self.group_cards[i+1].card_value:
                    if i == 0:
                        if self.group_cards[i+1].card_value !=self.group_cards[i+2].card_value:
                            index_d.append(i)
                    elif i >0 and (i+2)<len(self.group_cards):
                        if self.group_cards[i+1].card_value !=self.group_cards[i+2].card_value and self.group_cards[i].card_value !=self.group_cards[i-1].card_value:
                            index_d.append(i)
                    elif i >0 and (i+2)==len(self.group_cards):
                        if self.group_cards[i].card_value !=self.group_cards[i-1].card_value:
                            index_d.append(i)
            if len(index_t) == n and len(index_d) == n:
                for index_i in range(len(index_t) - 1):
                    if self.group_cards[index_t[index_i]].card_value +1 != self.group_cards[index_t[index_i + 1]].card_value:
                        return False
                return True
            else:
                return False
        else:
            return False

    # 判断是否为四代两单
    def is_four_take_sigle(self):
        if len(self.group_cards) == 6:
            flag = 0
            for i in range(len(self.group_cards) - 1):
                if self.group_cards[i].card_value == self.group_cards[i+1].card_value:
                    flag += 1
                else:
                    flag = 0
                if flag == 3:
                    return True
            return False
        else:
            return False

    # 判断是否为四代两对
    def is_four_take_double(self):
        if len(self.group_cards) == 8:
            flag_f = 0
            for i in range(len(self.group_cards) - 1):
                if self.group_cards[i].card_value == self.group_cards[i+1].card_value:
                    flag_f += 1
                else:
                    flag_f = 0
                if flag_f == 3:
                    break
            # 找出对子个数
            index_d = []  # 对子的下标
            for i in range(len(self.group_cards) - 1):
                if self.group_cards[i].card_value == self.group_cards[i + 1].card_value:
                    if i == 0:
                        if self.group_cards[i+1].card_value !=self.group_cards[i+2].card_value:
                            index_d.append(i)
                    elif i >0 and (i+2)<len(self.group_cards):
                        if self.group_cards[i+1].card_value !=self.group_cards[i+2].card_value and self.group_cards[i].card_value !=self.group_cards[i-1].card_value:
                            index_d.append(i)
                    elif i >0 and (i+2)==len(self.group_cards):
                        if self.group_cards[i].card_value !=self.group_cards[i-1].card_value:
                            index_d.append(i)
            if flag_f == 3 and len(index_d) == 2:
                return True
            else:
                return False
        else:
            return False

    def judge_group_type(self):
        #先按照牌值排序
        self.group_cards = sorted(self.group_cards, key=lambda card: card.card_value)

        if len(self.group_cards) == 1:
            self.group_type = 1
        elif len(self.group_cards) == 2:
            if self.group_cards[0].card_value == self.group_cards[1].card_value:#对子
                self.group_type = 2
            elif self.group_cards[0].card_value == 14 and self.group_cards[1].card_value ==15:#王炸
                self.group_type = 14
            elif self.group_cards[0].card_value == 15 and self.group_cards[1].card_value ==14:#王炸
                self.group_type = 14
            else:
                self.group_type = -1
        elif len(self.group_cards) == 3:
            if self.group_cards[0].card_value == self.group_cards[2].card_value:#3条
                self.group_type = 3
        elif len(self.group_cards) == 4:
            if self.group_cards[0].card_value == self.group_cards[3].card_value:#炸弹
                self.group_type = 13
            elif self.group_cards[0].card_value == self.group_cards[2].card_value or self.group_cards[1].card_value == self.group_cards[3].card_value :#三带一单
                self.group_type = 7
            else:
                self.group_type = -1
        elif len(self.group_cards) == 5:
            if self.is_sigle_line():#单连
                self.group_type = 4
            elif self.group_cards[0].card_value == self.group_cards[1].card_value and self.group_cards[2].card_value == self.group_cards[4].card_value: #三带一对
                self.group_type = 8
            elif self.group_cards[0].card_value == self.group_cards[2].card_value and self.group_cards[3].card_value == self.group_cards[4].card_value: #三带一对
                self.group_type = 8
            else:
                self.group_type = -1
        elif len(self.group_cards) == 6:
            if self.is_sigle_line():#单连
                self.group_type = 4
            elif self.is_double_line():#对连
                self.group_type = 5
            elif self.is_three_line():#三连
                self.group_type = 6
            elif self.is_four_take_sigle():#四带两单
                self.group_type = 11
            else:
                self.group_type = -1
        elif len(self.group_cards) == 7:
            if self.is_sigle_line():#单连
                self.group_type = 4
            else:
                self.group_type = -1
        elif len(self.group_cards) == 8:
            if self.is_sigle_line():#单连
                self.group_type = 4
            elif self.is_double_line():#对连
                self.group_type = 5
            elif self.is_aircraft_single_card():#飞机带单
                self.group_type = 9
            elif self.is_four_take_double():#四代两对
                self.group_type = 12
            else:
                self.group_type = -1
        elif len(self.group_cards) == 9:
            if self.is_sigle_line():#单连
                self.group_type = 4
            elif self.is_three_line():#三连
                self.group_type = 6
            elif self.is_aircraft_single_card():#飞机带单
                self.group_type = 9
            else:
                self.group_type = -1
        elif len(self.group_cards) == 10:
            if self.is_sigle_line():#单连
                self.group_type = 4
            elif self.is_double_line():#对连
                self.group_type = 5
            elif self.is_aircraft_double_card():#飞机带对
                self.group_type = 10
            else:
                self.group_type = -1
        elif len(self.group_cards) == 11:
            if self.is_sigle_line():  # 单连
                self.group_type = 4
            else:
                self.group_type = -1
        elif len(self.group_cards) == 12:
            if self.is_double_line():#对连
                self.group_type = 5
            elif self.is_three_line():#三连
                self.group_type = 6
            elif self.is_aircraft_single_card():#飞机带单
                self.group_type = 9
            else:
                self.group_type = -1
        elif len(self.group_cards) == 13:
            self.group_type = -1
        elif len(self.group_cards) == 14:
            if self.is_double_line():#对连
                self.group_type = 5
            else:
                self.group_type = -1
        elif len(self.group_cards) == 15:
            if self.is_aircraft_double_card():  # 飞机带对
                self.group_type = 10
            else:
                self.group_type = -1
        elif len(self.group_cards) == 16:
            if self.is_double_line():#对连
                self.group_type = 5
            elif self.is_aircraft_single_card():#飞机带单
                self.group_type = 9
            else:
                self.group_type = -1
        elif len(self.group_cards) == 17:
            self.group_type = -1
        elif len(self.group_cards) == 18:
            if self.is_double_line():#对连
                self.group_type = 5
            else:
                self.group_type = -1
        elif len(self.group_cards) == 19:
            self.group_type = -1
        elif len(self.group_cards) == 20:
            if self.is_double_line():#对连
                self.group_type = 5
            elif self.is_aircraft_double_card():#飞机带对
                self.group_type = 10
            else:
                self.group_type = -1

    #获取该组合牌的防守价值和攻击价值（1.0版，暂不考虑"对手"手牌数、已出牌的顺序等信息）
    def get_group_DA_value(self,dark_cards):
        dark_cards = sorted(dark_cards, key=lambda card: card.card_value)
        bomb_count_pro_count = self.get_bomb_count(dark_cards)
        if self.group_type == 1:
            self.attack_value,self.attack_value = self.get_sigle_DA_value(dark_cards)
        elif self.group_type == 2:
            self.attack_value, self.attack_value = self.get_double_DA_value(dark_cards)
        elif self.group_type == 3:
            self.attack_value, self.attack_value = self.get_three_DA_value(dark_cards)


    #获取暗牌中可能存在炸弹的个数
    def get_bomb_count(self,dark_cards):
        index = 0
        bomb_count = 0
        king_bomb_flag = 0
        while index < len(dark_cards):
            # 获取该暗牌值共有几张
            same_value_card_count = 1
            for j in range(4):
                if dark_cards[index].card_value == dark_cards[index + j + 1].card_value:
                    same_value_card_count += 1
                else:
                    break
            if same_value_card_count == 4:
                bomb_count = bomb_count+1
            index = index +same_value_card_count-1
        for card in dark_cards:
            if card.card_value >13:
                king_bomb_flag+=1;
        if king_bomb_flag ==2:
            bomb_count = bomb_count + 1
        return bomb_count

    def get_sigle_DA_value(self,dark_cards):
        defense_count = 0
        attack_count = 0
        for card in dark_cards:
            if self.group_cards[0].card_value > card.card_value:
                defense_count += 1
            elif self.group_cards[0].card_value < card.card_value:
                attack_count += 1
        return defense_count,attack_count

    def get_double_DA_value(self,dark_cards):
        defense_count = 0
        attack_count = 0
        index = 0
        while index <len(dark_cards):
            same_value_card_count = 1
            # 获取该暗牌值共有几张
            for j in range(4):
                if dark_cards[index].card_value == dark_cards[index + j + 1].card_value:
                    same_value_card_count += 1
                else:
                    break
            if same_value_card_count > 1:
                if self.group_cards[0].card_value > dark_cards[index].card_value:
                   defense_count = defense_count + int(same_value_card_count*(same_value_card_count-1)/2)#c_n_2
                elif self.group_cards[0].card_value < dark_cards[index].card_value:
                    attack_count = attack_count + int(same_value_card_count * (same_value_card_count - 1) / 2)  # c_n_2
            index = index + same_value_card_count
        return defense_count,attack_count

    def get_three_DA_value(self,dark_cards):
        defense_count = 0
        attack_count = 0
        index = 0
        while index <len(dark_cards):
            same_value_card_count = 1
            # 获取该暗牌值共有几张
            for j in range(4):
                if dark_cards[index].card_value == dark_cards[index + j + 1].card_value:
                    same_value_card_count += 1
                else:
                    break
            if same_value_card_count > 2:
                if self.group_cards[0].card_value > dark_cards[index].card_value:
                    defense_count = defense_count + int(same_value_card_count*(same_value_card_count-1)*(same_value_card_count-2)/6)#c_n_3
                elif self.group_cards[0].card_value < dark_cards[index].card_value:
                    attack_count = attack_count + int(
                        same_value_card_count * (same_value_card_count - 1)*(same_value_card_count - 2) / 6)  # c_n_3
            index = index + same_value_card_count
        return defense_count,attack_count

    def get_sigle_line_DA_value(self,dark_cards):
        dark_cards = sorted(dark_cards, key=lambda card: card.card_value)
        group_card_count = len(self.group_cards)
        top_card_value = self.group_cards[-1].card_value;
        defense_count = 0
        attack_count = 0

        #将暗牌中的A、2、大小王删除
        new_dark_cards = []
        for card in dark_cards:
            if card.card_value>2 and card.card_value<14:
                new_dark_cards.append(card)

        divide_index_up = -1
        divide_index_down = -1
        #在'暗牌'中找到'分界'位置
        for card in new_dark_cards:
            if card.card_value >top_card_value:
                break
            else:
                divide_index_up +=1

        for card in new_dark_cards:
            if card.card_value <top_card_value:
                divide_index_down += 1
            else:
                break


        #比组合拍（单连）小的所有单连
        samal_lines = []
        for i in range(3+group_card_count-1,top_card_value,1):
            samal_line = []
            for j in range(3,i+1,1):
                samal_line.append(j)
            samal_lines.append(samal_line)

        # 比组合拍（单连）大的所有单连
        big_lines = []
        for i in range(top_card_value, 14, 1):
            big_line = []
            for j in range(i-group_card_count, i , 1):
                big_line.append(j)
                big_lines.append(big_line)

        #根据可能的单连得到获取的'概率'
        for s_line in samal_lines:
            defense_count_tmp = 1
            for card_value in s_line:
                n = self.find_card_count(card_value,new_dark_cards)
                if n >0:
                    defense_count_tmp = defense_count_tmp*n
                else:
                    defense_count_tmp = 0
            defense_count = defense_count + defense_count_tmp

        for b_lines in big_lines:
            attack_count_tmp = 1
            for card_value in b_lines:
                n = self.find_card_count(card_value,new_dark_cards)
                if n >0:
                    attack_count_tmp = attack_count_tmp * n
                else:
                    attack_count_tmp = 0
            attack_count = attack_count + attack_count_tmp

        return defense_count, attack_count


    def find_card_count(self,card_value,target_cards):
        n = 0
        for card in target_cards:
            if card.card_value == card_value:
                n += 1
        return n