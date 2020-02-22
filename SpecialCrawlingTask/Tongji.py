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
Informal_GAV_List = []

def read():
    global wangying_todo_gradle,wangying_todo_maven, kaifeng_todo
    wangying_todo_gradle = JSONFIle_processing.read( wangying_todo_gradle_path )
    wangying_todo_maven = JSONFIle_processing.read( wangying_todo_maven_path )
    kaifeng_todo = JSONFIle_processing.read(kaifeng_tofo_path)


def compare():
    global  wangying_todo_gradle,wangying_todo_maven, kaifeng_todo, Task_todo_list, Informal_GAV_List

    # print(wangying_todo_gradle)
    # print(wangying_todo_maven)
    # print(kaifeng_todo)

    aLLtodo = []
    aLLtodo.extend( wangying_todo_gradle )
    aLLtodo.extend( wangying_todo_maven )
    aLLtodo.extend( kaifeng_todo )
    # huizong
    for ele in aLLtodo:
        try:
            groupId = ele["groupId"]
            artifactId = ele["artifactId"]
            version = ele["version"]
            # ele = {"groupId":groupId,"artifactId":artifactId,"version":version}
            new_ele = {"groupId":groupId,"artifactId":artifactId,"version":version}

            if new_ele not in Task_todo_list:
                Task_todo_list.append(new_ele)
        except:
            continue

    print("length: wangying_todo_gradle todo", len(wangying_todo_gradle))
    print("length: wangying_todo_maven todo", len(wangying_todo_maven))
    print("length: kaifeng_todo", len(kaifeng_todo))
    print("length: Original_AllValid_Todo_GAV", len( Task_todo_list ))

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
        print(ele)
        try:
            groupId = ele["groupId"]
            artifactId = ele["artifactId"]
            version = ele["version"]

            full_path = jar_path + GA_folder_map[groupId + '__fdse__' + artifactId] + '/' + version +'/'
            if os.path.exists(full_path):
                print("Existing full_path: ", full_path)
                continue

            else:
                print("not Existing full_path: ", full_path)
                count_less += 1
                Existing_todo_list.append(ele)
        except:
            count_informl += 1
            Informal_GAV_List.append( ele )
            continue

    print("count_informl: ", count_informl)
    print("Existing_Todo_GAV_List: ",count_less)

    JSONFIle_processing.write(Task_todo_list,'Local_Data/Original_AllValid_Todo_GAV.json')
    JSONFIle_processing.write(Existing_todo_list,"Local_Data/Existing_Todo_GAV_List.json")
    JSONFIle_processing.write(Informal_GAV_List, "Local_Data/Informal_GAV_List.json")


def main_Serve():
    read()
    compare()

if __name__ == '__main__':
    main_Serve()