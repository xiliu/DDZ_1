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
        if group_type == 4:
            self.get_all_single_line()



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
            if self.hand_cards[idx_b].card_value > 2 and self.hand_cards[idx_b].card_value < 14 and self.hand_cards[
                idx_e].card_value > 2 and self.hand_cards[idx_e].card_value < 14:
                while idx_e<n:
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
        print("总共有"+str(len(trees))+'棵树')
        trees_good = []
        for tree in trees:
            if tree.get_deep_count()>4:
                trees_good.append(tree)
        print('筛选符合要求的树有'+str(len(trees_good))+'课')
        for tree in trees_good:
            print('深度为：',tree.get_deep_count())
            tree.detail()

        for tree in trees_good:
            self.get_single_line_from_tree(tree)
    def get_single_line_from_tree(self,tree):
        print('---get_single_line_from_tree---')
        deepth = tree.get_deep_count()

        for line_count in range(5,deepth+1):
            pro_group_count = tree.get_pro_count()
