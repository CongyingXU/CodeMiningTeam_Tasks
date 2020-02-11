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
    with open('Local_Data/Format_GAList_Num_mt_1500.json','r') as f:
        GA_list = json.loads( f.read() )

def generateFile():

    global GA_list
    task_cursor = 10400
    for ele in GA_list:
        ele = int(ele)
        if ele < task_cursor:
            continue
        else:
                task_item = "/home/fdse/wangying/crawled_data/__fdse__/home/fdse/wangying/CrawlLibraries/data/" + "__fdse__" + str(
                    ele) + "__fdse__" + str(ele + 1)
                task_content["Task_Todo"].append(task_item)
                # task_cursor = ele + 2

    with open("Local_Data/Todo_CMDorTask0208.json",'w') as f:
        f.write( json.dumps( task_content,indent=4 ) )
read()
generateFile()
