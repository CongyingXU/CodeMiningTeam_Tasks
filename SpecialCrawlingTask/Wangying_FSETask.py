# -*- coding: utf-8 -*-

"""
Created on 2020-02-23 18:06  

@author: congyingxu
"""
from CommonFunction import JSONFIle_processing


GA_V_path = 'Local_Data/lib_versions__wangying.json'
Todo_GAV_List_path = "Local_Data/Todo_GAV_List__fdse__lib_versions_wangying.json"
Todo_GAV_List = []

# read
GA_V = JSONFIle_processing.read( GA_V_path )

# collect
for ele in GA_V:
    lib = ele["lib"]
    versions = ele["versions"]
    for version in versions:
        todo_item = {}
        todo_item["groupId"] = lib.split("__fdse__")[0]
        todo_item["artifactId"] = lib.split("__fdse__")[1]
        todo_item["version"] = version
        todo_item["type"] = "jar"

        Todo_GAV_List.append(todo_item)

# write()
print( "Todo_GAV_List len: " , len(Todo_GAV_List))
JSONFIle_processing.write(Todo_GAV_List,Todo_GAV_List_path)

