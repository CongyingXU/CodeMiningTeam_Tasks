# -*- coding: utf-8 -*-

"""
Created on 2020-01-18 12:21  

@author: congyingxu
"""

import json

task_start = 2010
task_end = 2100
task_maxCount = 10


task_content = { "Task_Todo":[]}
GA_list = []
def read():
    global GA_list
    with open('Data/Format_GAList_Num.json','r') as f:
        GA_list = json.loads( f.read() )

def generateFile():

    global GA_list
    for ele in GA_list:
        ele = int(ele)
        if ele < 4500:
            continue
        else:
                task_item = "/home/fdse/wangying/crawled_data/__fdse__/home/fdse/wangying/CrawlLibraries/data/" + "__fdse__" + str(
                    ele) + "__fdse__" + str(ele + 2)
                task_content["Task_Todo"].append(task_item)

    with open("Data/Todo_CMDorTask.json",'w') as f:
        f.write( json.dumps( task_content,indent=4 ) )
read()
generateFile()
