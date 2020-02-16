# -*- coding: utf-8 -*-

"""
Created on 2020-02-13 00:14  

@author: congyingxu

统计一下，有多少重叠部分
"""

import json

GAV_mt_1000IC = {}
GAV_mt_1500 = {}
jar = []


All_gav = 0
crawled_gav = 0

def read():
    global GAV_mt_1000IC,GAV_mt_1500,jar

    GAV_mt_1000IC_path = 'Local_Data/gav_mt_1000_ic.json'
    GAV_mt_1500_path = 'Local_Data/gav_mt_1500.json'
    jar_path = 'Local_Data/jars.json'

    with open(GAV_mt_1000IC_path,'r') as f:
        GAV_mt_1000IC = json.loads(   f.read() )

    with open(GAV_mt_1500_path,'r') as f:
        GAV_mt_1500 = json.loads(   f.read() )

    with open(jar_path, 'r') as f:
        jar = json.loads(f.read())


def collect():
    global All_gav,crawled_gav

    # for GA in GAV_mt_1000IC.keys():
    #     A = GA.split("__fdse__")[1]
    #     for V in GAV_mt_1000IC[GA]:

    for GA in GAV_mt_1500.keys():
        A = GA.split("__fdse__")[1]
        for V in GAV_mt_1500[GA]:


            All_gav += 1

            AV_name = GA.split("__fdse__")[1] + "-" + V + ".jar"

            # print(AV_name)
            if AV_name in jar:
                crawled_gav +=1


More_GA_count = 0
More_GAV_count = 0

def collect0215():
    global More_GA_count, More_GAV_count


    for GA in GAV_mt_1000IC.keys():

        if GA in GAV_mt_1500.keys():
            for V in GAV_mt_1000IC[GA]:
                if V in GAV_mt_1500[GA]:
                    continue
                else:
                    More_GAV_count += 1
        else:
            # print(GA)
            More_GA_count += 1
            More_GAV_count += len( GAV_mt_1000IC[GA] )





read()
# collect()
# print("GAV_mt_1500:  ",crawled_gav , All_gav)

collect0215()
print("More_GA_count: ",More_GA_count)
print("More_GAV_count: ",More_GAV_count)