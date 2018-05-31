# coding: utf-8

import itertools
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
        if group_type == 14: #王炸
            self.get_king_bomb()
        # if group_type == 4:
        #     self.get_all_single_line()
        if group_type == 5:
            self.get_all_double_line()



    def get_all_single(self):
        for card in self.hand_cards:
            group = Group([card])
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
                group = Group([self.hand_cards[item[0]],self.hand_cards[item[1]]])
                self.hand_groups.append(group)
            elif same_value_count > 2:
                for i in range(same_value_count):
                    for j in range(i+1,same_value_count,1):
                        group = Group([self.hand_cards[item[i]],self.hand_cards[item[j]]])
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
                    group = Group(group_card)
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
            group = Group([self.hand_cards[item[0]], self.hand_cards[item[1]], self.hand_cards[item[2]], self.hand_cards[item[3]]])
            self.hand_groups.append(group)

    def get_king_bomb(self):
        king_card = []
        for card in self.hand_cards:
            if card.card_value >13:
                king_card.append(card)

        if len(king_card) == 2:
            group = Group([king_card[0], king_card[1]])
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
                self.hand_groups.append(Group(line))
                #self.get_sub_single_line(line)


    def get_sub_single_line(self,path):
        # logger.info('获取子单连')
        path_l = len(path)
        if path_l>5:
            for n in range(5,path_l):
                for i in range(path_l-n+1):
                    self.hand_groups.append(Group(path[i:i+n]))


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

        print('-------所有相等的牌------')
        for same_item in all_same_card:
            for card in same_item:
                card.detail()
            print("")

        # 过滤掉连续量小于3个的
        series_begin_index =0
        all_same_card_series = []
        for i in range(len(all_same_card)):
            if i < len(all_same_card) - 2:
                if all_same_card[i][0].card_value +1 != all_same_card[i+1][0].card_value:
                    if i - series_begin_index>1:#联系值大于等于3个
                        all_same_card_series.append(all_same_card[series_begin_index:i+1])
                    series_begin_index = i+1

            elif i == len(all_same_card) - 2:
                if all_same_card[i][0].card_value + 1 == all_same_card[i + 1][0].card_value or (all_same_card[i][0].card_value ==13 and all_same_card[i+1][0].card_value==1):
                    if (i - series_begin_index +1)>1:#联系值大于等于3个
                        all_same_card_series.append(all_same_card[series_begin_index:i+2])
                        series_begin_index = i+2
                else:
                    if (i - series_begin_index) > 1:  # 联系值大于等于3个
                        all_same_card_series.append(all_same_card[series_begin_index:i + 1])
                        series_begin_index = i + 1
        print('-------过滤后满足3连的牌------')
        for card_series in all_same_card_series:
            for same_cards in card_series:
                for card in same_cards:
                    card.detail()
            print("")
        print('----------------------')