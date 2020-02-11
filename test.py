#!/usr/bin/env python
# encoding: utf-8
"""

Created on 2019/12/2 16:47
@Author : CongyingXu

"""
import math
print('hello world')

# n = 1
# while True:
#     N = 0
#     for num in range(7):
#         N += math.pow(n,num)
#
#     result  = 381/N
#     print(381 / N,n)
#     if int(result) == result:
#         break
#     else:
#         n+=1


import os
import time

def loop_Server():
    count = 0
    while True:

        cmd = "python C:\\Users\\Congy\\PycharmProjects\\CodeMiningTeam_Tasks\\Client_Main.py CongyingXu_win"
        os.system(cmd)
        print("Count: ",count)

        sleep_time = 60*60 * 3 #3h
        time.sleep(sleep_time)
        count+=1


loop_Server()