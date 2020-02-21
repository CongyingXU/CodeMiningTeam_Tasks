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

# jar_path = "/Users/congyingxu/Downloads/CrawledGAVs_0218/"
jar_path = "/home/hadoop/dfs/data/Workspace/CongyingXU/Passport/Processed_Downloads_Jars/CrawledGAVs_0218/"

kaifeng_tofo_path = "Local_Data/kaifeng_FSE_harmo_gav.json"
wangying_todo_gradle_path = "Local_Data/wangying_FSE_Todo_GAV_List_gradle.json"
wangying_todo_maven_path = "Local_Data/wangying_FSE_Todo_GAV_List_maven.json"


wangying_todo_gradle = []
wangying_todo_maven = []

Task_todo_list =  []
Existing_todo_list = []

def read():
    global wangying_todo_gradle,wangying_todo_maven, kaifeng_tofo
    wangying_todo_gradle = JSONFIle_processing.read( wangying_todo_gradle_path )
    wangying_todo_maven = JSONFIle_processing.read( wangying_todo_maven_path )
    kaifeng_tofo = JSONFIle_processing.read(kaifeng_tofo_path)


def compare():
    global  wangying_todo_gradle,wangying_todo_maven, kaifeng_tofo, Task_todo_list


    # huizong todo
    for ele in wangying_todo_gradle:
        if ele not in Task_todo_list:
            Task_todo_list.append( ele )
    for ele in wangying_todo_maven:
        if ele not in Task_todo_list:
            Task_todo_list.append( ele )
    for ele in kaifeng_tofo:
        if ele not in Task_todo_list:
            Task_todo_list.append( ele )


    # get need todo
    existing_Jars_full_list = len( File_processing.walk_FileDir(jar_path) )
    print("Jars_num: ", existing_Jars_full_list)

    GA_folder_list = File_processing.walk_L1_Folders(jar_path)
    GA_folder_map = {}
    for folder in GA_folder_list:
        GA = folder.split("__fdse__")[0] +'__fdse__'+ folder.split("__fdse__")[1]
        GA_folder_map[GA]= folder


    count_less = 0

    for ele in Task_todo_list:
        try:
            groupId = ele["groupId"]
            artifactId = ele["artifactId"]
            version = ele["version"]

            full_path = jar_path + GA_folder_map[groupId + '__fdse__' + artifactId] + '/' + version +'/'

            if os.path.exists(full_path):
                continue
            else:
                count_less += 1
                Existing_todo_list.append(ele)
        except:
            continue

    print(count_less)

    JSONFIle_processing.write(Task_todo_list,'Local_Data/Original_All_Todo_GAV_List.json')
    JSONFIle_processing.write(Existing_todo_list,"Local_Data/Existing_Todo_GAV_List.json")


def main_Serve():
    # read()
    compare()

if __name__ == '__main__':
    main_Serve()