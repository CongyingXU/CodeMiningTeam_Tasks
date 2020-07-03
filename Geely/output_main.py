# -*- coding: utf-8 -*-

"""
Created on 2020-01-11 18:46

@author: congyingxu

used to collect poj's dependencies
"""

import os
import sys
import json
import time
from terminaltables import AsciiTable,PorcelainTable

# data_folder_path = "/Users/congyingxu/Downloads/CodeMiningTeam_Tasks/GenerateDG/poj_DG_data/data/dependency/raw/"
# data_folder_path = sys.argv[1]
data_folder_path = "/Users/congyingxu/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/7bbb49018d9f0a8252e0bc7b45cb81f8/Message/MessageTemp/3ba8fe614cd0ab6239dda289db7c257c/File/openapi-admin_2020-04-23/"

separator = " "

poj_dependency_filenames = []
ALL_Data = {}
GA_usge_Data = {}

poj_list = set()
G_list = set()
GA_list = set()
GAV_list = set()

GAV_poj_amount = {}
GA_poj_amount ={} # amount of pojs employing GA
GA_V_amount = {} # amount of GA version employed

# rootdir -> list: all filenames in Level 1
def walk_L1_FileNames():
    global poj_dependency_filenames
    for parent, dirnames, filenames in os.walk(data_folder_path):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        poj_dependency_filenames =  filenames

def collect_dependency():
    global ALL_Data,poj_list,G_list,GA_list,GAV_list,conn,cursor
    id = 0
    for filename in poj_dependency_filenames:
        file_path = data_folder_path + filename

        if file_path.endswith(".DS_Store"):
            continue
        with open(file_path,'r') as f:
            poj_dependency = json.loads( f.read())

        poj = filename
        # if poj in ALL_Data.keys()
        ALL_Data[poj] = {}
        if poj not in poj_list:
            poj_list.add(poj)
        for ele in poj_dependency:
            keys = ele.keys()
            if "groupId" not in keys or "artifactId" not in keys or "version" not in keys or "type" not in keys:
                continue
            if '$' in ele["groupId"] or '$' in ele["artifactId"] or '$' in ele["version"] or '$' in ele["type"]:
                continue
            if "classifier" in keys and '$' in ele["classifier"]:
                continue
            id += 1
            groupId = ele["groupId"]
            artifactId = ele["artifactId"]
            type = ele["type"]
            version = ele["version"]


            if groupId in ALL_Data[poj].keys():
                if artifactId in ALL_Data[poj][groupId].keys():
                    if version in ALL_Data[poj][groupId][artifactId].keys():
                        ALL_Data[poj][groupId][artifactId][version] =  ALL_Data[poj][groupId][artifactId][version] +1
                    else:
                        ALL_Data[poj][groupId][artifactId].update( {version:1} )
                else:
                    ALL_Data[poj][groupId].update( {artifactId:{version:1}} )
            else:
                ALL_Data[poj].update( {groupId:{artifactId:{version:1}}} )

            GA = groupId +separator+ artifactId
            if GA in GA_usge_Data.keys():
                if version in GA_usge_Data[GA].keys():
                    if poj in GA_usge_Data[GA][version].keys():
                        GA_usge_Data[GA][version][poj] = GA_usge_Data[GA][version][poj] + 1
                    else:
                        GA_usge_Data[GA][version].update({poj: 1})
                else:
                    GA_usge_Data[GA].update( {version:{poj:1}} )
            else:
                GA_usge_Data.update( {GA:{version:{poj:1}}} )



            groupId = ele["groupId"]
            artifactId = ele["artifactId"]
            type = ele["type"]
            version = ele["version"]

            G_list.add(groupId)
            GA_list.add(groupId+separator+artifactId)
            GAV_list.add(groupId+separator+artifactId+separator+version)

    poj_list = list(poj_list)
    G_list = list(G_list)
    GA_list = list(GA_list)
    GAV_list = list(GAV_list)

    # dumpsJSON(GAV_list, "GAV_list.json")
    # dumpsJSON(ALL_Data, "P_GAV_data.json")



    # with open("poj_list.json",'r') as f:
    #     poj_list = json.loads( f.read() )
    # pGAV_data = {}
    # for poj in ALL_Data.keys():
    #     index0 = poj_list.index(poj[:-len("_2020-01-08.json")])
    #     pGAV_data[str(index0)] = ALL_Data[poj]

    # dumpsJSON(pGAV_data, "GAV_data.json")









def prepare_data():
    start_time = time.time()
    walk_L1_FileNames()
    walk_L1_FileNames_time = time.time()
    # print("walk_L1_FileNames time: ", time.time() - start_time)

    collect_dependency()
    collect_dependency_time = time.time()
    # print("collect_dependency time: ", collect_dependency_time - walk_L1_FileNames_time)

def output_TopN_used_GA():
    global GA_poj_amount,GA_V_amount,GAV_poj_amount

    for GA in GA_list:
        version_dict = GA_usge_Data[GA]
        GA_V_amount[GA] = len(version_dict)
        GA_poj_amount[GA] = set()
        for V in version_dict.keys():
            GAV = GA + separator + V
            GAV_poj_amount[GAV] = len(GA_usge_Data[GA][V])
            GA_poj_amount[GA] |= set(GA_usge_Data[GA][V].keys())
        GA_poj_amount[GA] = len(GA_poj_amount[GA])

    l = [[v, k] for k, v in GA_V_amount.items()]  # list comprehensions
    GA_V_amount_list = sorted(l, reverse=True)
    l = [[v, k] for k, v in GA_poj_amount.items()]  # list comprehensions
    GA_poj_amount_list = sorted(l, reverse=True)
    l = [[v, k] for k, v in GAV_poj_amount.items()]  # list comprehensions
    GAV_poj_amount_list = sorted(l, reverse=True)

    # print
    print()
    # 被项目使用最多的library。 Amount of project：使用该library的项目总数， Library (GA)：为GroupID ArtifactID
    print("Top 10 popular libraries used by projects")
    print_TopN_used_GA([ ["Amount of project","Library (GA)"] ] +GA_poj_amount_list)
    print()
    # 被使用的版本最多的library。 Amount of version：该library被使用的版本总数， Library (GA)：为GroupID ArtifactID
    print("Top 10 libraries used in different versions")
    print_TopN_used_GA([ ["Amount of version","Library (GA)"] ] +GA_V_amount_list)
    print()
    # 被项目使用最多的特定版本的library。 Amount of project：使用该library该版本的项目总数， Library (GAV)：为GroupID ArtifactID Version
    print("Top 10 popular libraries in certain versions")
    print_TopN_used_GA([ ["Amount of project","Library (GAV)"] ] +GAV_poj_amount_list)



def print_TopN_used_GA(table_data):
    min_amount = table_data[10 -1][0]
    min_amount = 10
    for ele in table_data[1:]:
        # print(ele[0],min_amount)
        str_gezi = "#" * int(ele[0]/min_amount)
        ele.append(str_gezi)
    table = AsciiTable(table_data[:20])
    print(table.table)

def dumpsJSON(data,path):
    with open(path,'w') as f:
        f.write( json.dumps(data,indent=4) )

def main():
    prepare_data()
    output_TopN_used_GA()





if __name__ == '__main__':
    main()