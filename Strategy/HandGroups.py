# coding: utf-8

import itertools
import Utils.basic_util as basic_util
from Utils.Cartesian import *
from Strategy.Group import *
from Strategy.Tree import *
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HandGroups:
    def __init__(self,hand_cards):
        #hand_cards = sorted(hand_cards, key=lambda card: card.card_value)
        self.hand_cards = hand_cards
        self.hand_groups = []

        for i in range(14):
            self.find_groups(i+1)

    def detail(self):
        for hand_group in self.hand_groups:
            hand_group.detail()
            print('')
        print("手牌总共有可能牌型"+str(len(self.hand_groups))+"种...")

    def find_groups(self,group_type):
        if group_type == 1:
            self.get_all_single()
        if group_type == 2:
            self.get_all_double()
        if group_type == 3:
            self.get_all_three()
        if group_type == 13: #炸弹
            self.get_all_bomb()
            self.get_all_four_take_single_card() # 四带两单
            self.get_all_four_take_double_card() # 四带两对
        if group_type == 14: #王炸
            self.get_king_bomb()
        if group_type == 4:
            self.get_all_single_line()
        if group_type == 5:   #对连
            self.get_all_double_line()
        if group_type == 6:   #三连（飞机不带）
            self.get_all_three_line()
        if group_type == 7:   #三带一
            self.get_all_three_take_one()
        if group_type == 8:  # 三带一对
            self.get_all_three_take_double()
        if group_type == 9:  # 飞机带单牌
            self.get_all_aircraft_single_card()
        if group_type == 10:  # 飞机带单牌
            self.get_all_aircraft_double_card()

    def get_all_single(self):
        for card in self.hand_cards:
            group = Group([card],group_type=1)
            self.hand_groups.append(group)

    def get_all_double(self):
        all_same_value_card_index = []
        idx = 0
        n = len(self.hand_cards)
        while idx < n:
            same_value_card_index = []
            same_value_card_index.append(idx)
            for j in range(3):
                if (idx + j + 1)< n and self.hand_cards[idx].card_value == self.hand_cards[idx + j + 1].card_value:
                    same_value_card_index.append(idx + j + 1)
                else:
                    break
            if len(same_value_card_index)>1:
                all_same_value_card_index.append(same_value_card_index)
                idx = idx + len(same_value_card_index)
            else:
                idx = idx+1

        for item in all_same_value_card_index:
            same_value_count = len(item)
            if same_value_count == 2:
                group = Group([self.hand_cards[item[0]],self.hand_cards[item[1]]],group_type=2)
                self.hand_groups.append(group)
            elif same_value_count > 2:
                for i in range(same_value_count):
                    for j in range(i+1,same_value_count,1):
                        group = Group([self.hand_cards[item[i]],self.hand_cards[item[j]]],group_type=2)
                        self.hand_groups.append(group)

    def get_all_three(self):
        all_same_value_card_index = []
        idx = 0
        n = len(self.hand_cards)
        while idx < n:
            same_value_card_index = []
            same_value_card_index.append(idx)
            for j in range(3):
                if (idx + j + 1)< n and self.hand_cards[idx].card_value == self.hand_cards[idx + j + 1].card_value:
                    same_value_card_index.append(idx + j + 1)
                else:
                    break
            if len(same_value_card_index)>1:
                all_same_value_card_index.append(same_value_card_index)
                idx = idx + len(same_value_card_index)
            else:
                idx = idx+1

        for item in all_same_value_card_index:
            same_value_count = len(item)
            if same_value_count >2:
                group_idx = list(itertools.combinations(item, 3))
                for group_item_idx in group_idx:
                    group_card = []
                    for idx in group_item_idx:
                        group_card.append(self.hand_cards[idx])
                    group = Group(group_card,group_type=3)
                    self.hand_groups.append(group)

    def get_all_bomb(self):
        all_same_value_card_index = []
        idx = 0
        n = len(self.hand_cards)
        while idx < n:
            same_value_card_index = []
            same_value_card_index.append(idx)
            for j in range(3):
                if (idx + j + 1) < n and self.hand_cards[idx].card_value == self.hand_cards[idx + j + 1].card_value:
                    same_value_card_index.append(idx + j + 1)
                else:
                    break
            if len(same_value_card_index) == 4:
                all_same_value_card_index.append(same_value_card_index)
                idx = idx + len(same_value_card_index)
            else:
                idx = idx + 1

        for item in all_same_value_card_index:
            group = Group([self.hand_cards[item[0]], self.hand_cards[item[1]], self.hand_cards[item[2]], self.hand_cards[item[3]]],group_type=13)
            self.hand_groups.append(group)

    def get_king_bomb(self):
        king_card = []
        for card in self.hand_cards:
            if card.card_value >13:
                king_card.append(card)

        if len(king_card) == 2:
            group = Group([king_card[0], king_card[1]],group_type=14)
            self.hand_groups.append(group)


    def get_all_single_line(self):
        #思路，直接遍历生成树，然后遍历树
        trees =[]
        idx_b = 0

        n = len(self.hand_cards)
        tree_b_index= 0 #从tree_b_index树开始添加新的叶子节点

        while idx_b < n:
            same_card_index = []
            same_card_index.append(idx_b)
            idx_e = idx_b + 1
            if self.hand_cards[idx_b].card_value != 2 and self.hand_cards[idx_b].card_value < 14 :
                while idx_e<n and self.hand_cards[idx_e].card_value > 2 and self.hand_cards[idx_e].card_value < 14:
                    if self.hand_cards[idx_e-1].card_value == self.hand_cards[idx_e].card_value:
                        same_card_index.append(idx_e)
                        idx_e += 1
                    elif self.hand_cards[idx_e-1].card_value != self.hand_cards[idx_e].card_value:
                        break

                #创建树的节点
                same_card_count = len(same_card_index)
                leaves_node = []
                for idx in same_card_index:
                    leaves_node.append(Node_card(self.hand_cards[idx]))
                if idx_b == 0:
                    for i in range(same_card_count):
                        tree = Tree(self.hand_cards[same_card_index[i]])
                        trees.append(tree)
                elif idx_b > 0:
                    if self.hand_cards[idx_b-1].card_value+1 == self.hand_cards[idx_b].card_value:
                        for t_idx in range(tree_b_index,len(trees)):
                            trees[t_idx].add_leaf(leaves_node)
                    else:#创建新的树根节点
                        tree_b_index = len(trees)
                        for i in range(same_card_count):
                            tree = Tree(self.hand_cards[same_card_index[i]])
                            trees.append(tree)
                idx_b = idx_e
            else:
                idx_b += 1
                continue

        #从树中选去连牌
        logger.info("总共有"+str(len(trees))+'棵树')
        trees_good = []
        for tree in trees:
            if tree.get_deep_count()>4:
                trees_good.append(tree)
            #tree.detail()
        logger.info('筛选符合要求的树有'+str(len(trees_good))+'课')
        for tree in trees_good:
            logger.info('深度为：'+str(tree.get_deep_count()))
            # tree.detail()

        for tree in trees_good:
            single_lines = tree.find_all_path()
            logger.info('len(single_line)='+str(len(single_lines)))
            for line in single_lines:
                self.hand_groups.append(Group(line,group_type=4))
                #self.get_sub_single_line(line)


    def get_sub_single_line(self,path):
        # logger.info('获取子单连')
        path_l = len(path)
        if path_l>5:
            for n in range(5,path_l):
                for i in range(path_l-n+1):
                    self.hand_groups.append(Group(path[i:i+n],group_type=4))


    def get_all_double_line(self):
        idx_b = 0
        n = len(self.hand_cards)
        all_same_card = []
        while idx_b < n:
            same_card_index = []
            same_card_index.append(idx_b)
            idx_e = idx_b + 1
            if self.hand_cards[idx_b].card_value != 2 and self.hand_cards[idx_b].card_value < 14:
                while idx_e < n and self.hand_cards[idx_e].card_value != 2 and self.hand_cards[idx_e].card_value < 14:
                    if self.hand_cards[idx_e - 1].card_value == self.hand_cards[idx_e].card_value:
                        same_card_index.append(idx_e)
                        idx_e += 1
                    elif self.hand_cards[idx_e - 1].card_value != self.hand_cards[idx_e].card_value:
                        break
            same_card_count = len(same_card_index)
            if same_card_count>1:
                same_card = []
                for idx in same_card_index:
                    same_card.append(self.hand_cards[idx])
                all_same_card.append(same_card)
            idx_b = idx_e

        # print('-------所有相等的牌------')
        # for same_item in all_same_card:
        #     for card in same_item:
        #         card.detail()
        #     print("")

        # 过滤掉连续量小于3个的，并将不同"多牌"连分开
        series_begin_index =0
        all_same_card_series = []
        for i in range(len(all_same_card)):
            if i < len(all_same_card) - 2:
                if all_same_card[i][0].card_value +1 != all_same_card[i+1][0].card_value:
                    if i - series_begin_index>1:#连续值大于等于3个
                        all_same_card_series.append(all_same_card[series_begin_index:i+1])
                    series_begin_index = i+1
            elif i == len(all_same_card) - 2:
                if all_same_card[i][0].card_value + 1 == all_same_card[i + 1][0].card_value or (all_same_card[i][0].card_value ==13 and all_same_card[i+1][0].card_value==1):
                    if (i - series_begin_index +1)>1:#连续值大于等于3个
                        all_same_card_series.append(all_same_card[series_begin_index:i+2])
                        series_begin_index = i+2
                else:
                    if (i - series_begin_index) > 1:  # 连续值大于等于3个
                        all_same_card_series.append(all_same_card[series_begin_index:i + 1])
                        series_begin_index = i + 1

        all_sub_same_card_series = []
        #将多牌序列量大于3的序列，找出满足条件的子序列
        for card_series in all_same_card_series:
            n = len(card_series)
            if n>3:
                for sub_count in range(3,n):#子序列个数3，4...n
                    for b_idx in range(n-sub_count+1):#起始下标
                        all_sub_same_card_series.append(copy.deepcopy(card_series[b_idx:b_idx+sub_count]))

        if len(all_sub_same_card_series) >1:
            all_same_card_series.extend(all_sub_same_card_series)

            # print('-------过滤后子‘多牌’连的牌------')
            # for card_series in all_sub_same_card_series:
            #     for same_cards in card_series:
            #         for card in same_cards:
            #             card.detail()
            #     print("")
            # print('----------------------')

        # print('-------过滤后满足大于等于3连的牌------')
        # for card_series in all_same_card_series:
        #     for same_cards in card_series:
        #         for card in same_cards:
        #             card.detail()
        #     print("")
        # print('----------------------')

        #从不同的"多牌"序列中组合不同的"对牌连"
        all_double_series = []
        for card_series in all_same_card_series:#变量不同"多牌"序列
            all_double_card = [] #将"多牌"序列中的"多牌"转换成所有可能的对牌
            for same_cards in card_series:
                double_cards = list(itertools.combinations(same_cards, 2))
                all_double_card.append(double_cards)

            cartesian = Cartesian(all_double_card)
            all_double_series.extend(cartesian.assemble())

        for double_serie in all_double_series:
            group_double_card = []
            for same_cards in double_serie:
                for card in same_cards:
                    group_double_card.append(card)
            self.hand_groups.append(Group(group_double_card,group_type=5))


        # print('-------所有对子连------')
        # for double_serie in all_double_series:
        #     for same_cards in double_serie:
        #         for card in same_cards:
        #             card.detail()
        #     print('')
        # print('---------------------')

    def get_all_three_line(self):
        # print("--------get_all_three_line-------")
        # for hand_group in self.hand_groups:
        #     # print(hand_group.group_type)
        #     if hand_group.group_type == 3:
        #         hand_group.detail()
        #         print('')
        # print("--------------------------")

        # #获取连续"飞机"牌，数据结构 [[[group(♠3 ♣3 ♦3 ),group(♠3 ♣3 ♥3 )],[group(♠4 ♣4 ♦4 )]],[[group(♠J ♣J ♦J ))],[group(♠Q ♣Q ♦Q )]]]
        all_series_group = []
        series_group = []   #一个满足"飞机"的连续牌，可能可以组合多个"飞机"牌
        same_value_group = [] #存放相同值得"三牌"组
        for hand_group in self.hand_groups:
            if hand_group.group_type == 3 and 2 < hand_group.group_cards[0].card_value < 14:
                if len(same_value_group) ==0:
                    same_value_group.append(tuple(copy.deepcopy(hand_group.group_cards)))
                else:
                    if same_value_group[-1][0].card_value == hand_group.group_cards[0].card_value:
                        same_value_group.append(tuple(copy.deepcopy(hand_group.group_cards)))
                    elif same_value_group[-1][0].card_value+1 == hand_group.group_cards[0].card_value:
                        series_group.append(same_value_group)
                        same_value_group = []
                        same_value_group.append(tuple(copy.deepcopy(hand_group.group_cards)))
                    else:
                        if len(series_group) == 0:
                            same_value_group = []
                            same_value_group.append(tuple(copy.deepcopy(hand_group.group_cards)))
                        elif len(series_group) > 0 and series_group[-1][-1][0].card_value +1 == same_value_group[-1][0].card_value:
                            series_group.append(same_value_group)
                            all_series_group.append(series_group)

                            series_group = []
                            same_value_group = []
                            same_value_group.append(tuple(copy.deepcopy(hand_group.group_cards)))

        if len(series_group) > 0 and series_group[-1][-1][0].card_value + 1 == same_value_group[-1][0].card_value:
            series_group.append(same_value_group)
            all_series_group.append(series_group)


        all_three_series = []

        #当有序列数大于2时，找出所有子序列，如序列数为4（3，3，3-4，4，4-5，5，5-6，6，6 出现的概率很低），则找出子序列数为2，3的序列
        #TODO..

        #获取每个序列的所有组合
        for item_series_group in all_series_group:
            cartesian = Cartesian(item_series_group)
            all_three_series.extend(cartesian.assemble())

        for three_serie in all_three_series:
            group_three_card = []
            for same_cards in three_serie:
                for card in same_cards:
                    group_three_card.append(card)
            self.hand_groups.append(Group(group_three_card,group_type=6))

    #三带一
    def get_all_three_take_one(self):
        all_single_group =[]
        all_three_group =[]
        for hand_group in self.hand_groups:
            if hand_group.group_type == 3:
                all_three_group.append(hand_group)
            elif hand_group.group_type == 1:
                all_single_group.append(hand_group)

        for three_group in all_three_group:
            three_group_cards = three_group.group_cards
            for single_group in all_single_group:
                three_take_one_cards = []
                if three_group_cards[0].card_value != single_group.group_cards[0].card_value: #排除"自己带自己"的问题
                    three_take_one_cards.extend(three_group_cards)
                    three_take_one_cards.extend(single_group.group_cards)
                    self.hand_groups.append(Group(three_take_one_cards, group_type=7))

    #三带二
    def get_all_three_take_double(self):
        all_double_group =[]
        all_three_group =[]
        for hand_group in self.hand_groups:
            if hand_group.group_type == 3:
                all_three_group.append(hand_group)
            elif hand_group.group_type == 2:
                all_double_group.append(hand_group)

        for three_group in all_three_group:
            three_group_cards = three_group.group_cards
            for double_group in all_double_group:
                three_take_one_cards = []
                if three_group_cards[0].card_value != double_group.group_cards[0].card_value: #排除"自己带自己"的问题
                    three_take_one_cards.extend(three_group_cards)
                    three_take_one_cards.extend(double_group.group_cards)
                    self.hand_groups.append(Group(three_take_one_cards, group_type=8))

    #飞机带单
    def get_all_aircraft_single_card(self):
        all_single_group = []
        all_aircraft_group = []
        for hand_group in self.hand_groups:
            if hand_group.group_type == 6:
                all_aircraft_group.append(hand_group)
            elif hand_group.group_type == 1:
                all_single_group.append(hand_group)

        for three_group in all_aircraft_group:
            tmp_single_group = []
            aircraft_group_cards = three_group.group_cards

            for single_group in all_single_group:#去掉三连牌中的单牌
                is_same = False
                for card in aircraft_group_cards:
                    if single_group.group_cards[0].card_value == card.card_value:
                        is_same = True
                if not is_same:
                    tmp_single_group.append(single_group)

            n = int(len(aircraft_group_cards)/3)
            group_list = list(itertools.combinations(tmp_single_group, n)) #获得组合
            for single_group in group_list:
                single_card = []
                for g in single_group:
                    single_card.extend(g.group_cards)
                aircraft_single_card = []
                aircraft_single_card.extend(aircraft_group_cards)
                aircraft_single_card.extend(single_card)
                self.hand_groups.append(Group(aircraft_single_card, group_type=9))

    # 飞机带对
    def get_all_aircraft_double_card(self):
        all_double_group = []
        all_aircraft_group = []
        for hand_group in self.hand_groups:
            if hand_group.group_type == 6:
                all_aircraft_group.append(hand_group)
            elif hand_group.group_type == 2:
                all_double_group.append(hand_group)

        for aircraft_group in all_aircraft_group:
            tmp_double_group = []
            aircraft_group_cards = aircraft_group.group_cards

            for double_group in all_double_group:  # 去掉三连牌中的单牌
                is_same = False
                for card in aircraft_group_cards:
                    if double_group.group_cards[0].card_value == card.card_value:
                        is_same = True
                if not is_same:
                    tmp_double_group.append(double_group)

            n = int(len(aircraft_group_cards) / 3)
            if len(tmp_double_group) >= n:
                group_list = list(itertools.combinations(tmp_double_group, n))  # 获得组合
                for d_group in group_list:
                    d_card = []
                    for g in d_group:
                        d_card.extend(g.group_cards)
                    aircraft_single_card = []
                    aircraft_single_card.extend(aircraft_group_cards)
                    aircraft_single_card.extend(d_card)
                    self.hand_groups.append(Group(aircraft_single_card, group_type=10))

    # 四带两单
    def get_all_four_take_single_card(self):
        all_single_group = []
        all_bomb_group = []
        for hand_group in self.hand_groups:
            if hand_group.group_type == 13:
                all_bomb_group.append(hand_group)
            elif hand_group.group_type == 1:
                all_single_group.append(hand_group)

        for bomb_group in all_bomb_group:
            tmp_single_group = []
            bomb_group_cards = bomb_group.group_cards

            for single_group in all_single_group:  # 去掉炸弹牌中的单牌
                is_same = False
                for card in bomb_group_cards:
                    if single_group.group_cards[0].card_value == card.card_value:
                        is_same = True
                if not is_same:
                    tmp_single_group.append(single_group)

            group_list = list(itertools.combinations(tmp_single_group, 2))  # 获得组合
            for single_group in group_list:
                single_card = []
                for g in single_group:
                    single_card.extend(g.group_cards)
                bomb_take_single_card = []
                bomb_take_single_card.extend(bomb_group_cards)
                bomb_take_single_card.extend(single_card)
                self.hand_groups.append(Group(bomb_take_single_card, group_type=11))

    # 四带两对
    def get_all_four_take_double_card(self):
        all_double_group = []
        all_bomb_group = []
        for hand_group in self.hand_groups:
            if hand_group.group_type == 13:
                all_bomb_group.append(hand_group)
            elif hand_group.group_type == 2:
                all_double_group.append(hand_group)

        for bomb_group in all_bomb_group:
            tmp_double_group = []
            bomb_group_cards = bomb_group.group_cards

            for double_group in all_double_group:  # 去掉炸弹牌中的对子牌
                is_same = False
                for card in bomb_group_cards:
                    if double_group.group_cards[0].card_value == card.card_value:
                        is_same = True
                if not is_same:
                    tmp_double_group.append(double_group)

            group_list = list(itertools.combinations(tmp_double_group, 2))  # 获得组合
            for d_group in group_list:
                d_card = []
                for g in d_group:
                    d_card.extend(g.group_cards)
                bomb_double_card = []
                bomb_double_card.extend(bomb_group_cards)
                bomb_double_card.extend(d_card)
                self.hand_groups.append(Group(bomb_double_card, group_type=12))
