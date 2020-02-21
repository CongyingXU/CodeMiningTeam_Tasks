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
file_path = "/home/hadoop/dfs/data/Workspace/projects_DG/harmo_gav.json"
ele_list = []

count_less = 0


def read():
    global ele_list
    with open(file_path,'r') as f:
        ele_list = json.loads( f.read() )
    # ele_list = JSONFIle_processing.read(file_path)

def compare():
    global count_less

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
        except:
            continue

    print(count_less)

def main_Serve():
    read()
    compare()

def main_taskFile():
    pass

if __name__ == '__main__':
    read()
    compare()