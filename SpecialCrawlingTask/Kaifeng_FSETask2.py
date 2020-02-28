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
Todo_GAV_List_path = "Local_Data/Todo_GAV_List__fdse__from_ic_ga.json"
ga_all_mt_1000_ic_NotInMaven_path = "Local_Data/ga_all_mt_1000_ic_NotInMaven.json"
# 之前已爬取的GAVinfo
Original_AllValid_Todo_GAV_path = "Local_Data/Original_AllValid_Todo_GAV.json"
ic_ga_path = "Local_Data/ic-ga.json"

gav_all_mt_1000_ic = []
ga_all_mt_1000_ic = []
ga_all_mt_1000_ic_NotInMaven = []
lib_versions = []
ic_ga = []


Original_AllValid_Todo_GAV = []
Todo_GAV_List = []

def read():
    global ga_all_mt_1000_ic, gav_all_mt_1000_ic, Todo_GAV_List, lib_versions, Original_AllValid_Todo_GAV, ic_ga
    gav_all_mt_1000_ic = JSONFIle_processing.read(gav_all_mt_1000_ic_path)
    lib_versions = JSONFIle_processing.read(lib_versions_path)
    Original_AllValid_Todo_GAV = JSONFIle_processing.read(Original_AllValid_Todo_GAV_path)
    ic_ga = JSONFIle_processing.read(ic_ga_path)


    print("gav_all_mt_1000_ic len: ", len(gav_all_mt_1000_ic) )
    print("Original_AllValid_Todo_GAV len: ", len(Original_AllValid_Todo_GAV) )

    # print( lib_versions )
count_int = 0

def collectData():
    global ga_all_mt_1000_ic, gav_all_mt_1000_ic, Todo_GAV_List, lib_versions, Original_AllValid_Todo_GAV, ga_all_mt_1000_ic_NotInMaven, ic_ga

    count_int = 0
    ## ga_all_mt_1000_ic
    ga_all_mt_1000_ic = set()
    for ele in gav_all_mt_1000_ic:
        try:
            groupId = ele["groupId"]
            artifactId = ele["artifactId"]
            GA = groupId + "__fdse__" + artifactId
            ga_all_mt_1000_ic.add(GA)
        except:
            print("ele not in gav_all_mt_1000_ic: ", ele)
            # continue
            break

    # write()
    ga_all_mt_1000_ic = ic_ga

    ## Todo_GAV_List
    for ele in lib_versions:
        lib = ele["lib"]
        GA = lib.split("__fdse__")[0] + "__fdse__" +  lib.split("__fdse__")[1]

        if GA in ga_all_mt_1000_ic:
            count_int += 1
            # print("GA in ga_all_mt_1000_ic", GA)
            for version in ele["versions"]:
                todo_item = {}
                todo_item["groupId"] = GA.split("__fdse__")[0]
                todo_item["artifactId"] = GA.split("__fdse__")[1]
                todo_item["version"] = version


                if todo_item in Original_AllValid_Todo_GAV:
                    # print("todo_item In Original_AllValid_Todo_GAV: ",todo_item)
                    continue
                else:
                    Todo_GAV_List.append(todo_item)
            # print("Todo_GAV_List", Todo_GAV_List)

        else:
            ga_all_mt_1000_ic_NotInMaven.append(GA)
            # print("GA not in ga_all_mt_1000_ic", GA )
            continue
            # break
    print("len ic_ga: ", len(ga_all_mt_1000_ic))
    print("count_int : ", count_int)
    print("count_task: ", len( Todo_GAV_List ))


def write():
    global ga_all_mt_1000_ic, gav_all_mt_1000_ic, Todo_GAV_List, lib_versions, Original_AllValid_Todo_GAV, ga_all_mt_1000_ic_NotInMaven

    ga_all_mt_1000_ic = list( ga_all_mt_1000_ic )
    ga_all_mt_1000_ic = list( set(ga_all_mt_1000_ic) )

    JSONFIle_processing.write(Todo_GAV_List,Todo_GAV_List_path)
    JSONFIle_processing.write(ga_all_mt_1000_ic, ga_all_mt_1000_ic_path)
    JSONFIle_processing.write(ga_all_mt_1000_ic_NotInMaven,ga_all_mt_1000_ic_NotInMaven_path)




if __name__ == '__main__':
    read()
    collectData()
    write()



# def cleanData():
#     content = JSONFIle_processing.read("Local_Data/kaifeng_FSE_harmo_gav.json")
#     for ele in content:
#         if ele["version"].startswith("${"):
#             print(ele)
#             content.remove(ele)
#     JSONFIle_processing.write(content,"Local_Data/kaifeng_FSE_harmo_gav.json")
#
# cleanData()