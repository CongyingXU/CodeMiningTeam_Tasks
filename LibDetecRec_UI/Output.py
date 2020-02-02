# -*- coding: utf-8 -*-

"""
Created on 2020-01-11 18:46  

@author: congyingxu

used to collect poj's dependencies
"""

import os
import json
import time
from terminaltables import AsciiTable,PorcelainTable
from collections import OrderedDict
import sqlite3
# conn = sqlite3.connect('DB/Dependency.db')
# cursor = conn.cursor()
data_folder_path = "/Users/congyingxu/Downloads/CodeMiningTeam_Tasks/GenerateDG/poj_DG_data/data/dependency/raw/"

separator = " "

poj_dependency_filenames = []
# ALL_Data = { P:{"GA_num":0,"GAV_num":0,G:{A:{V:usage_count}}} }
ALL_Data = {}
# GA_usge_Data = {GA:{ "poj_num":0,"version_num":0, "poj_list":[],"version_list":[] } }
# # GA_usge_Data = {GA:{ "poj_num":0,"version_num":0,"poj_set":poj_set,"version_set":version_set, V:{P:[usage_count]} } }
GA_usge_Data = {}



poj_list = set()
G_list = set()
GA_list = set()
GAV_list = set()


def mkTable():
    # + 删除旧表
    sql = 'create table PGAV (id int primary key, Project varchar(100), GroupID varchar(100), ArtifactID varchar(100), Version varchar(100) )'
    cursor.execute(sql)

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


            # insert
            # sql = "insert into PGAV (id,Project,GroupID,ArtifactID,Version) values (?,?,?,?,?)"
            # cursor.execute(sql, (id, poj, groupId, artifactId, version,) )



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

                        # GA_usge_Data[GA]["poj_set"] = GA_usge_Data[GA]["poj_set"].add(poj)
                        # GA_usge_Data[GA]["version_set"] = GA_usge_Data[GA]["version_set"].add(version)
                else:
                    GA_usge_Data[GA].update( {version:{poj:1}} )
                    # print(GA_usge_Data)
                    # GA_usge_Data[GA]["poj_set"] = GA_usge_Data[GA]["poj_set"].add(poj)
                    # GA_usge_Data[GA]["version_set"] = GA_usge_Data[GA]["version_set"].add(version)
            else:
                GA_usge_Data.update( {GA:{version:{poj:1}}} )

                # GA_usge_Data[GA].update({"poj_set": poj_set})
                # GA_usge_Data[GA].update ( {"version_set": version_set})

                # GA_usge_Data[GA]["poj_set"] = set()
                # GA_usge_Data[GA]["version_set"] = set()
                #
                # GA_usge_Data[GA]["poj_set"] = GA_usge_Data[GA]["poj_set"].add(poj)
                # GA_usge_Data[GA]["version_set"] = GA_usge_Data[GA]["version_set"].add(version)
                # print(GA_usge_Data)

                # GA_usge_Data[GA].update ( {"poj_num":1} )
                # GA_usge_Data[GA].update ( {"version_num": 1})



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
    GAV_list = list(GA_list)





def prepare_data():
    start_time = time.time()
    walk_L1_FileNames()
    walk_L1_FileNames_time = time.time()
    print("walk_L1_FileNames time: ", time.time() - start_time)

    collect_dependency()
    collect_dependency_time = time.time()
    print("collect_dependency time: ", collect_dependency_time - walk_L1_FileNames_time)

GAV_poj_amount = {}
GA_poj_amount ={} # amount of pojs employing GA
GA_V_amount = {} # amount of GA version employed



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

    # sort

    # sorted(GA_V_amount.items(), key=lambda d: d[1])
    # sorted(GA_poj_amount.items(), key=lambda d: d[1])
    # sorted(GAV_poj_amount.items(), key=lambda d: d[1])

    # print("GA_V_amount",len(GA_V_amount_list))
    # print(GA_V_amount_list[:15] )
    # print("GA_poj_amount",len(GA_poj_amount_list))
    # print(GA_poj_amount_list[:15] )
    # print("GAV_poj_amount",len(GAV_poj_amount_list))
    # print(GAV_poj_amount_list[:15] )


    # print
    print("GA_poj_amount")
    print_TopN_used_GA([ ["amount","GA"] ] +GA_poj_amount_list)
    print("GA_V_amount")
    print_TopN_used_GA([ ["amount","GA"] ] +GA_V_amount_list)
    print("GAV_poj_amount")
    print_TopN_used_GA([ ["amount","GAV"] ] +GAV_poj_amount_list)


    # GA_Usage = OrderedDict()
    # for GA in GA_list:
    #     G = GA.split( separator )[0]
    #     A = GA.split( separator )[1]
    #     sql = "select Version from PGAV where GroupID=? and ArtifactID=?"
    #     cursor.execute(sql, (G,A,))
    #     # cursor.execute(sql, (G, A,))
    #     # 获取查询结果：
    #     values = cursor.fetchall()  # 返回最终一次sql结果，列表元组形式   #[(1, 'ch.qos.logback', .....), (2, 'commons-cli', ...)]
    #     values_set = set(values)
    #     amount = len(values_set)
    #     GA_V_amount.update( {GA:amount} )
    #
    #     sql = "select Project from PGAV where GroupID=? and ArtifactID=?"
    #     cursor.execute(sql, (G, A,))
    #     # cursor.execute(sql, (G, A,))
    #     # 获取查询结果：
    #     values = cursor.fetchall()  # 返回最终一次sql结果，列表元组形式   #[(1, 'ch.qos.logback', .....), (2, 'commons-cli', ...)]
    #     values_set = set(values)
    #     amount = len(values_set)
    #     GA_poj_amount.update({GA: amount})
    #


def print_TopN_used_GA(table_data):
    # print(type(table_data))
    # table_data = [ ['Heading1', 'Heading2'], ['row1 column1', 'row1 column2'], ['row2 column1', 'row2 column2'], ['row3 column1', 'row3 column2'] ]
    min_amount = table_data[10 -1][0]
    min_amount = 10
    for ele in table_data[1:]:
        # print(ele[0],min_amount)
        str_gezi = "#" * int(ele[0]/min_amount)
        ele.append(str_gezi)
    table = AsciiTable(table_data[:10])
    print(table.table)

def dumpsJSON(data,path):
    with open(path,'w') as f:
        f.write( json.dumps(data,indent=4) )

def main():
    prepare_data()

    start_time = time.time()
    output_TopN_used_GA()
    output_TopN_used_GA_time = time.time()
    print("output_TopN_used_GA time: ", output_TopN_used_GA_time - start_time)




    # write
    dumpsJSON(ALL_Data,"DB/PGAV.json")
    dumpsJSON(GA_usge_Data, "DB/GAVP.json")
    dumpsJSON(poj_list, "DB/P_list.json")
    dumpsJSON(G_list, "DB/G_list.json")
    dumpsJSON(GA_list, "DB/GA_list.json")
    dumpsJSON(GAV_list, "DB/GAV_list.json")
    dumpsJSON(GAV_poj_amount, "DB/GAV_poj_amount.json")
    dumpsJSON(GA_poj_amount, "DB/GA_poj_amount.json")
    dumpsJSON(GA_V_amount, "DB/GA_V_amount.json")


    # output_TopN_used_GAV()
    # output_GA_usedV_range()


    # # 关闭游标：
    # cursor.close()
    # # 提交事物
    # conn.commit()
    # # 关闭连接
    # conn.close()


# mkTable()
main()





def output_TopN_used_GAV():
    pass

def output_GA_usedV_range():
    pass