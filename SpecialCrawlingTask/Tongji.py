# -*- coding: utf-8 -*-

"""
Created on 2020-02-21 10:25  

@author: congyingxu
"""
from CommonFunction import JSONFIle_processing, File_processing


import sys
sys.path.append('../')  # 新加入的

# file+path


jar_path = "home/hadoop/dfs/data/Workspace/CongyingXU/Passport/Processed_Downloads_Jars/CrawledGAVs_0218/"
file_path = "/home/hadoop/dfs/data/Workspace/projects_DG/harmo_gav.json"
ele_list = []

count_less = 0


def read():
    global ele_list
    ele_list = JSONFIle_processing.read(file_path)

def compare():
    global count_less
    for ele in ele_list:
        try:
            groupId = ele["groupId"]
            artifactId = ele["artifactId"]
            version = ele["version"]

            full_path = jar_path + groupId + '__fdse__' + artifactId + '/' + version +'/'

            if File_processing.pathExist(full_path):
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