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
kaifeng_todo = []

Task_todo_list =  []
Existing_todo_list = []

def read():
    global wangying_todo_gradle,wangying_todo_maven, kaifeng_todo
    wangying_todo_gradle = JSONFIle_processing.read( wangying_todo_gradle_path )
    wangying_todo_maven = JSONFIle_processing.read( wangying_todo_maven_path )
    kaifeng_todo = JSONFIle_processing.read(kaifeng_tofo_path)


def compare():
    global  wangying_todo_gradle,wangying_todo_maven, kaifeng_todo, Task_todo_list



    # huizong
    for ele in wangying_todo_gradle:
        if ele not in Task_todo_list:
            Task_todo_list.append( ele )
    print("length: wangying_todo_gradle todo", len(wangying_todo_gradle))
    for ele in wangying_todo_maven:
        if ele not in Task_todo_list:
            Task_todo_list.append( ele )
    print("length: wangying_todo_maven todo", len(wangying_todo_maven))
    for ele in kaifeng_todo:
        if ele not in Task_todo_list:
            Task_todo_list.append( ele )
    print("length: kaifeng_todo", len(kaifeng_todo))
    print("length: Original_All_Todo_GAV", len( Task_todo_list ))

    # get need
    existing_Jars_full_list = len( File_processing.walk_FileDir(jar_path) )
    print("Jars_num: ", existing_Jars_full_list)

    GA_folder_list = File_processing.walk_L1_Folders(jar_path)
    GA_folder_map = {}
    for folder in GA_folder_list:
        GA = folder.split("__fdse__")[0] +'__fdse__'+ folder.split("__fdse__")[1]
        GA_folder_map[GA]= folder


    count_less = 0
    count_informl = 0

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
            count_informl += 1

            continue

    print(count_informl)

    print("Existing_Todo_GAV_List: ",count_less)

    JSONFIle_processing.write(Task_todo_list,'Local_Data/Original_All_Todo_GAV_List.json')
    JSONFIle_processing.write(Existing_todo_list,"Local_Data/Existing_Todo_GAV_List.json")


def main_Serve():
    read()
    compare()

if __name__ == '__main__':
    main_Serve()