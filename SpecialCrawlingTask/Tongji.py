# -*- coding: utf-8 -*-

"""
Created on 2020-02-21 10:25  

@author: congyingxu
"""



import sys,os
sys.path.append('../')  # 新加入的
from CommonFunction import JSONFIle_processing, File_processing

import json
# file+path


jar_path = "/home/hadoop/dfs/data/Workspace/CongyingXU/Passport/Processed_Downloads_Jars/CrawledGAVs_0218/"
# file_path = "/home/hadoop/dfs/data/Workspace/projects_DG/harmo_gav.json"
# file_path = "/Users/congyingxu/Desktop/harmo_gav.json"
file_path = '/home/hadoop/dfs/data/Workspace/CongyingXU/gav_all_mt_1000_ic.json'

task_file_path = 'Local_Data/gav_all_mt_1000_ic.json'
task_list = []
ele_list = []


Task_todo_list =  []

count_less = 0


def read():
    global ele_list,task_list
    with open(file_path,'r') as f:
        ele_list = json.loads( f.read() )
    # ele_list = JSONFIle_processing.read(file_path)
    # task_list = JSONFIle_processing.read(task_file_path)

def compare():
    global count_less,Task_todo_list

    Jars_num = len( File_processing.walk_FileDir(jar_path) )
    print("Jars_num: ", Jars_num)

    GA_folder_list = File_processing.walk_L1_Folders(jar_path)
    GA_folder_map = {}
    for folder in GA_folder_list:
        GA = folder.split("__fdse__")[0] +'__fdse__'+ folder.split("__fdse__")[1]
        GA_folder_map[GA]= folder

    for ele in ele_list:
        try:
            groupId = ele["groupId"]
            artifactId = ele["artifactId"]
            version = ele["version"]

            full_path = jar_path + GA_folder_map[groupId + '__fdse__' + artifactId] + '/' + version +'/'


            if os.path.exists(full_path):
                continue
            else:
                count_less += 1
                # print(file_path)
                Task_todo_list.append(ele  )
        except:
            continue

    print(count_less)
    # JSONFIle_processing.write(Task_todo_list,'Todo_GAV_List.json')




def compare_tasks():
    global count_less

    for ele in ele_list:
        try:
            groupId = ele["groupId"]
            artifactId = ele["artifactId"]
            version = ele["version"]

            if ele in task_list:
                pass
            else:
                count_less += 1
        except:
            continue


    print(count_less)

def main_taskFile():
    read()
    compare_tasks()

def main_Serve():
    read()
    compare()

if __name__ == '__main__':
    main_Serve()