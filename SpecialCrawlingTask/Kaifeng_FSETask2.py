# -*- coding: utf-8 -*-

"""
Created on 2020-02-22 13:59  

@author: congyingxu

新策略： 根据GA爬取 GAV
"""


from CommonFunction import File_processing, JSONFIle_processing


gav_all_mt_1000_ic_path = "Local_Data/gav_all_mt_1000_ic.json"
ga_all_mt_1000_ic_path = "Local_Data/ga_all_mt_1000_ic.json"
lib_versions_path = "Local_Data/lib_versions.json"
Todo_GAV_List_path = "Local_Data/Todo_GAV_List__fdse__from_ga_all_mt_1000_ic.json"
# 之前已爬取的GAVinfo
Original_All_Todo_GAV_List_path = "Local_Data/Original_All_Todo_GAV_List.json"

gav_all_mt_1000_ic = []
ga_all_mt_1000_ic = []
lib_versions = []


Original_All_Todo_GAV_List = []
Todo_GAV_List = []

def read():
    global ga_all_mt_1000_ic, gav_all_mt_1000_ic, Todo_GAV_List, lib_versions, Original_All_Todo_GAV_List
    ga_all_mt_1000_ic = JSONFIle_processing.read(ga_all_mt_1000_ic_path)
    gav_all_mt_1000_ic = JSONFIle_processing.read(gav_all_mt_1000_ic_path)
    lib_versions = JSONFIle_processing.read(lib_versions_path)
    Original_All_Todo_GAV_List = JSONFIle_processing.read(Original_All_Todo_GAV_List_path)


def collectData():
    global ga_all_mt_1000_ic, gav_all_mt_1000_ic, Todo_GAV_List, lib_versions, Original_All_Todo_GAV_List

    ## ga_all_mt_1000_ic
    ga_all_mt_1000_ic = set()
    for ele in gav_all_mt_1000_ic:
        try:
            groupId = ele["groupId"]
            artifactId = ele["artifactId"]
            GA = groupId + "__fdse__" + artifactId
            ga_all_mt_1000_ic.add(GA)
        except:
            continue

    ## Todo_GAV_List
    for ele in lib_versions:
        lib = ele["lib"]
        GA = lib.split("__fdse__")[0] + "__fdse__" +  lib.split("__fdse__")[1]

        if GA in ga_all_mt_1000_ic:
            print("GA in ga_all_mt_1000_ic", GA)
            for version in ele["versions"]:
                todo_item = {}
                todo_item["groupId"] = GA.split("__fdse__")[0]
                todo_item["artifactId"] = GA.split("__fdse__")[1]
                todo_item["version"] = version

                if todo_item in Original_All_Todo_GAV_List:
                    print("todo_item In Original_All_Todo_GAV_List: ",todo_item)
                    continue
                else:
                    Todo_GAV_List.append(todo_item)
                    print("Todo_GAV_List", Todo_GAV_List)
        else:
            print("GA not in ga_all_mt_1000_ic", GA )


def write():
    global ga_all_mt_1000_ic, gav_all_mt_1000_ic, Todo_GAV_List
    global ga_all_mt_1000_ic, gav_all_mt_1000_ic, Todo_GAV_List, lib_versions, Original_All_Todo_GAV_List


if __name__ == '__main__':
    read()
    collectData()
    write()