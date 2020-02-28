# -*- coding: utf-8 -*-

"""
Created on 2020-01-17 23:19  

@author: congyingxu
过滤得：Geely 所使用的GA
"""

import json

GA_list = set()
GA_list_Num = []
GAV_list = []
Original_GAV_list = []
GA_list_InCentralRepo = []
GA_list_NotInCentralRepo = []

lib_versions = []

def read():
    global Original_GAV_list,lib_versions
    with open('Wangying_FSEData/GAV_list.json','r') as f:
        Original_GAV_list = json.loads( f.read() )
    with open('Wangying_FSEData/lib_versions.json','r') as f:
        lib_versions = json.loads( f.read() )




def collect_data():
    global GA_list,GAV_list,Original_GAV_list,lib_versions,GA_list_Num,GA_list_InCentralRepo,GA_list_NotInCentralRepo
    for GAV in Original_GAV_list:
        if GAV.startswith("aaa") or "aaa" in GAV:
            continue
        else:
            GAV_list.append(GAV)
            GA = GAV.split(' ')[0] + "__fdse__" + GAV.split(' ')[1]
            GA_list.add(GA)




    GA_list = list(GA_list)
    for i in range(len(lib_versions)):
        GA_ele = lib_versions[i]["lib"][:-14]
        if GA_ele in GA_list:
            # GA_list_Num.append( (i,GA_ele) )
            GA_list_Num.append(i)
            GA_list_InCentralRepo.append(GA_ele)


    for GA_ele in GA_list:
        if GA_ele in GA_list_InCentralRepo:
            pass
        else:
            GA_list_NotInCentralRepo.append(GA_ele)


    print("GA_list",len(GA_list))
    print("GA_list_Num",len(GA_list_Num))







def write():

    with open('Wangying_FSEData/Format_GAVList.json','w') as f:
        f.write( json.dumps( GAV_list,indent=4 ) )

    with open('Wangying_FSEData/Format_GAList.json','w') as f:
        f.write( json.dumps( GA_list,indent=4 ) )

    with open('Wangying_FSEData/Format_GAList_Num.json','w') as f:
        f.write( json.dumps( GA_list_Num,indent=4 ) )

    with open('Wangying_FSEData/Format_GAList_InCentralRepo.json','w') as f:
        f.write( json.dumps( GA_list_InCentralRepo,indent=4 ) )

    with open('Wangying_FSEData/Format_GAList_NotInCentralRepo.json','w') as f:
        f.write( json.dumps( GA_list_NotInCentralRepo,indent=4 ) )

if __name__ == '__main__':
    read()
    collect_data()
    write()
