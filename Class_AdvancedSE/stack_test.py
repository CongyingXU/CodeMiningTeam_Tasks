# -*- coding: utf-8 -*-

"""
Created on 2020-01-19 17:21  

@author: congyingxu
"""
from Class_AdvancedSE import stack_implement

stack_int = stack_implement.SimpleStack()

# test, 测试元素1 是否压栈成功
def Testpush():
    global stack_int

    push_ele = 1
    stack_int.push(push_ele)
    if stack_int.peek() == push_ele:
        print("successfully pushing ele!")
    else:
        print("sth wrong with pushing ele!")


# test，测试堆栈不为空时，是否可以清空成功
def TestClean():
    global stack_int

    push_ele = 2
    stack_int.push(push_ele)
    stack_int.clean()
    if stack_int.size == 0:
        print("successfully cleaning!")
    else:
        print("sth wrong with cleaning!")
        return


# test，测试堆栈为空时，及压栈元素2后，是否可以弹栈成功
def Testpop():
    global stack_int

    stack_int.clean()
    pop_ele = stack_int.pop()
    if pop_ele == None:
        print("successfully popping None!")
    else:
        print("sth wrong with popping None!")
        return

    push_ele = 2
    stack_int.push(push_ele)
    pop_ele = stack_int.pop()
    if pop_ele == 2:
        print("successfully popping ele!")
    else:
        print("sth wrong with popping ele!")
        return


# test，测试在堆栈被清空时，及压栈元素2后，是否可以成功判断是否为空
def TestIsEmpty():
    global stack_int

    stack_int.clean()
    if stack_int.isEmpty() == True:
        print("successfully checking IsEmpty!")
    else:
        print("sth wrong with checking IsEmpty!")
        return

    push_ele = 2
    stack_int.push(push_ele)
    if stack_int.isEmpty() == False:
        print("successfully checking IsEmpty!")
    else:
        print("sth wrong with checking IsEmpty!")
        return


# test，测试堆栈压栈元素2后，是否可以成功返回栈顶元素
def TestPeek():
    global stack_int

    stack_int.clean()
    push_ele = 2
    stack_int.push(push_ele)
    if stack_int.peek() == 2:
        print("successfully peeking!")
    else:
        print("sth wrong with peeking!")
        return

def main():
    Testpush()
    TestClean()
    Testpop()
    TestPeek()
    TestIsEmpty()

if __name__ == '__main__':
    main()

