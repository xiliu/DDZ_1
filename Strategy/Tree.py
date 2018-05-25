import operator as op
import copy
class Tree:

    def __init__(self,card):
        self._head = Node_card(card)

    def insert(self, path, data):
        cur = self._head
        for step in path:
            if op.eq(cur.go(step),None):
                return False
            else:
                cur = cur.go(step)
        cur.add(Node_card(data))
        return True

    def search(self, path):
        cur = self._head
        for step in path:
            if op.eq(cur.go(step),None):
                return None
            else:
                cur = cur.go(step)
        return cur

    #增加叶子
    def add_leaf(self,leaf_datas):
        cur = self._head
        children_node = cur.getchildren()
        if len(children_node) == 0:
            for leaf_data in leaf_datas:
                cur.add(copy.deepcopy(leaf_data))
            return
        else:
            for begin_node in children_node:
                self._add_leaf(begin_node,leaf_datas,2)

    def _add_leaf(self,begin_node,leaf_datas,depth):
        children_node = begin_node.getchildren()
        if len(children_node) == 0:
            for leaf_data in leaf_datas:
                begin_node.add(copy.deepcopy(leaf_data)) #先深copy节点，在添加节点
            return
        else:
            for b_node in children_node:
                self._add_leaf(b_node,leaf_datas,depth+1)

    #获取树的深度
    def get_deep_count(self):
        if len(self._head.getchildren()) == 0:
            return 1
        else:
            return self._get_deep_count(self._head.getchildren()[0])+1

    def _get_deep_count(self,cur_node):
        children_node = cur_node.getchildren()
        if len(children_node) == 0:
            return 1
        else:
            return self._get_deep_count(children_node[0])+1

    #获取遍历树总共有多少种可能
    def get_pro_count(self,max_deepth):


    def detail(self):
        self._head.getdata().detail()
        print('')
        children = self._head.getchildren()
        if len(children)>0:
            self._breath_search(children)
    def _breath_search(self,children_node):
        print("-", end='')
        for node in children_node:
            node.getdata().detail()
            print("-", end='')
        print('')
        next_children_node = []
        for node in children_node:
            nodes = node.getchildren()
            for n in nodes:
                next_children_node.append(n)
        if len(next_children_node)>0:
            self._breath_search(next_children_node)
        else:
            return



class Node_card:

    def __init__(self, data_card):
        self._data_card = data_card
        self._children_card = []

    def getdata(self):
        return self._data_card

    def getchildren(self):
        return self._children_card

    def add(self, node):
        ##if full
        if len(self._children_card) > 4:
            return False
        else:
            self._children_card.append(node)

    def go(self, data):
        for child in self._children_card:
            if child.getdata().card_type == data.card_type and child.getdata().card_value == data.card_value:
                return child
        return None


# if __name__ == '__main__':
#
#     tree = tree()
#     tree.linktohead(a)
#
#     # testcase
#     print('Node', tree.search("ABE").getdata())
#     print('Node', tree.search("ABC").getdata())
#     print('Node', tree.search("AHM").getdata())
#     tree.insert("ABCD", 1)
#     for i in d.getchildren():
#         print('value after', d.getdata(), ' is ', i.getdata())
#
#     tree.detail(a)