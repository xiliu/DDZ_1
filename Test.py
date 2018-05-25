# coding: utf-8

from Card import *
from Poker import *
from Player import *
from Strategy.HandGroups import *
import numpy


def factorial(n,k):
    value = 1
    value_d = 1
    if k>0 and k<=n:
        for i in range(n+1,n+1-k,-1):
            value *=i;

        for i in range(k):
            value_d*=(i+1)
    else:
        print('参数不合法...')


    return int(value/value_d)

if __name__ == '__main__':

    print("------------------初始化牌-------------")
    poker = Poker(54)
    poker.detail()
    print("")
    print("------------------洗牌-------------")
    poker.shuffle()
    poker.detail()
    print("")
    print("------------------发牌-------------")

    players = []
    for i in range(3):
        cards = []
        for j in range(17):
            cards.append(poker.deal())

        player = Player(i+1,cards)
        players.append(player)

    for i in range(3):
        players[i].detail()
    print("")

    print("------------------玩家整理牌后---------")
    for i in range(3):
        players[i].order_cards()
        players[i].detail()
        print("------------------玩家手牌的所有可能组合---------")
        hand_cards = players[i].get_hand_cards()
        hand_groups = HandGroups(hand_cards)
        hand_groups.detail()



    # hand_cards_count = 17
    # pro_count = 0
    # for i in range(hand_cards_count):
    #     pro_count += factorial(hand_cards_count, i+1)
    # print("pro_count = "+str(pro_count))