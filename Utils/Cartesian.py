# -*- coding:utf-8 -*-
#------------笛卡尔积N个数组的排列组合--------------
'''
变量
datagroup : 表示n个list(python 中的list与其他编程中的数组定义类似)的集合,即一个二维数组
counterIndex：datagroup反向下标值
counter : 用来记录当前datagroup中每一个数组输出的下标，初始全为0，因为从第一个开始输出
'''

'''
方法 
countlength : 计算数组长度,即计算n的具体值 
handle ：处理datagoroup二维数组中每一个一维数组输出的下标值 
assemble ： 对datagoroup中的n个一维数组中的每一元素进行排列组合输出
'''

# python 实现N个数组的排列组合(笛卡尔积算法)
class Cartesian():
    # 初始化
    def __init__(self, datagroup):
        self.datagroup = datagroup
        # 二维数组从后往前下标值
        self.counterIndex = len(datagroup)-1
        # 每次输出数组数值的下标值数组(初始化为0)
        self.counter = [0 for i in range(0, len(self.datagroup))]

    # 计算数组长度
    def countlength(self):
        i = 0
        length = 1
        while(i < len(self.datagroup)):
            length *= len(self.datagroup[i])
            i += 1
        return length

    # 递归处理输出下标
    def handle(self):
        # 定位输出下标数组开始从最后一位递增
        self.counter[self.counterIndex]+=1
        # 判断定位数组最后一位是否超过长度，超过长度，第一次最后一位已遍历结束
        if self.counter[self.counterIndex] >= len(self.datagroup[self.counterIndex]):

            # 重置末位下标
            self.counter[self.counterIndex] = 0
            # 标记counter中前一位
            self.counterIndex -= 1
            # 当标记位大于等于0，递归调用
            if self.counterIndex >= 0:
                self.handle()
            # 重置标记
            self.counterIndex = len(self.datagroup)-1

    # 排列组合输出
    def assemble(self):
        all_combination = []
        length = self.countlength()
        i = 0
        while(i < length):
            attrlist = []
            j = 0
            while(j<len(self.datagroup)):
                attrlist.append(self.datagroup[j][self.counter[j]])
                j += 1
            # print (attrlist)
            all_combination.append(attrlist)
            self.handle()
            i += 1

        return all_combination


if __name__ == "__main__":
    # 构造二维数组
    datagroup = [[(13,23),(23,33)], [(14,34)], [(15,25), (25,35)]]
    for i in range(len(datagroup)):
        for j in range(len(datagroup[i])):
            print(datagroup[i][j])
            datagroup[i][j] = list(datagroup[i][j])
    # 创建cartesian对象
    cartesian = Cartesian(datagroup)
    cartesian.assemble()

    all_series = []
    all_series.extend(cartesian.assemble())

    for serie in all_series:
        print(serie)