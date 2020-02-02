# -*- coding: utf-8 -*-

"""
Created on 2020-01-19 16:48  

@author: congyingxu
"""

class SimpleStack:
    size = 0
    array = []

    # 压栈
    def push(self,ele):
        self.array.append(ele)
        self.size = len(self.array)

    # 出栈
    def pop(self):
        if self.size == 0:
            return None
        else:
            ele = self.array[-1]
            self.array = self.array[:-1]
            self.size = len(self.array)
            return ele

    # 为空
    def isEmpty(self):
        if self.size == 0:
            return True
        else:
            return False

    # 返回栈定元素值
    def peek(self):
        ele = self.array[-1]
        return ele

    # 清空
    def clean(self):
        self.array = []
        self.size = len(self.array)