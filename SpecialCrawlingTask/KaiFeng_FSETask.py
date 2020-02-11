# -*- coding: utf-8 -*-

"""
Created on 2020-02-06 20:02  

@author: congyingxu
"""

import json


GA_Todo = []
GA_list_Num = []
GA_list_InCentralRepo = []
lib_versions = {}
gav_json = []



def read():
    global lib_versions, gav_json
    with open("Local_Data/lib_versions.json",'r') as f:
        lib_versions = json.loads( f.read() )

    with open("Local_Data/gav_mt_1500.json", 'r') as f:
        gav_json = json.loads(f.read())



def process():
    global GA_Todo, GA_list_Num, GA_list_InCentralRepo
    GA_Todo = list( gav_json.keys() )
    for i in range(len(GA_Todo)):
        # print(GA_Todo[i])
        # GA_Todo[i] = GA_Todo[i][:-11]
        GA_Todo[i] = GA_Todo[i].split("__fdse__")[0] + "__fdse__" + GA_Todo[i].split("__fdse__")[1]
        # print(GA_Todo[i])


    for i in range(len(lib_versions)):
        GA_ele = lib_versions[i]["lib"][:-14]
        if GA_ele in GA_Todo:
            GA_list_Num.append(i)
            GA_list_InCentralRepo.append(GA_ele)

    for GA_ele in GA_Todo:
        if GA_ele not in GA_list_InCentralRepo:
            print("Not In : ", GA_ele)


def write():
    with open('Local_Data/Format_GAList_Num_mt_1500.json', 'w') as f:
        f.write(json.dumps(GA_list_Num, indent=4))

    # with open('Data/Format_GAList_InCentralRepo.json', 'w') as f:
    #     f.write(json.dumps(GA_list_InCentralRepo, indent=4))
    #
    # with open('Data/Format_GAList_NotInCentralRepo.json', 'w') as f:
    #     f.write(json.dumps(GA_list_NotInCentralRepo, indent=4))
    pass


if __name__ == '__main__':
    read()
    process()
    write()