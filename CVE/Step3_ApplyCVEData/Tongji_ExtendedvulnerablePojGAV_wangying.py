# -*- coding: utf-8 -*-

"""
Created on 2020-02-24 16:34  

@author: congyingxu

与颖姐那边的CVE数据会和一下，康康vulnerable poj and gav 是否有补充
"""


from CommonFunction import File_processing, JSONFIle_processing

affected_pojs_wangying_path = "Wangying_FSEData/affected_projs_wangying.json"
affected_pojs__wangying = []

used_vulne_libs_wangying_path = "Wangying_FSEData/used_vulne_libs_wangying.json"
used_vulne_libs_wangying = []

Vulnerable_dependency_from_pojs_path = "Vulnerable_dependency_fromPojs.json"
Vulnerable_dependency_from_pojs = {}

Extended_Vulnerable_dependency_from_pojs_path = "Wangying_FSEData/Extended_Vulnerable_dependency_fromPojs.json"
Extended_Vulnerable_dependency_from_pojs = {}


Extended_affected_pojs_path = "Wangying_FSEData/Extended_affected_pojs.json"
Extended_used_vulne_libs_path = "Wangying_FSEData/Extended_used_vulne_libs.json"
Extended_used_vulne_libs = {}
Extended_affected_pojs = []
Extended_used_ga = []


def read():
    global affected_pojs__wangying, used_vulne_libs_wangying, Vulnerable_dependency_from_pojs

    affected_pojs__wangying = JSONFIle_processing.read(affected_pojs_wangying_path)
    used_vulne_libs_wangying = JSONFIle_processing.read(used_vulne_libs_wangying_path)
    Vulnerable_dependency_from_pojs = JSONFIle_processing.read(Vulnerable_dependency_from_pojs_path)

def collectData():
    global affected_pojs__wangying, used_vulne_libs_wangying, Vulnerable_dependency_from_pojs, Extended_Vulnerable_dependency_from_pojs, Extended_used_vulne_libs, Extended_affected_pojs, Extended_used_ga

    for GA in Vulnerable_dependency_from_pojs.keys():
        if GA in used_vulne_libs_wangying.keys():

            for V in Vulnerable_dependency_from_pojs[GA].keys():
                if V in used_vulne_libs_wangying[GA]:
                    for poj in Vulnerable_dependency_from_pojs[GA][V]:
                        if poj not  in affected_pojs__wangying:
                            print(GA , V , poj)
                            print("Bu Ying Dang!!!!")
                    pass
                else:
                    if GA not in Extended_Vulnerable_dependency_from_pojs.keys():
                        Extended_Vulnerable_dependency_from_pojs[GA] = {}
                    Extended_Vulnerable_dependency_from_pojs[GA][V] = Vulnerable_dependency_from_pojs[GA][V]


        else:
            Extended_Vulnerable_dependency_from_pojs[GA] = Vulnerable_dependency_from_pojs[GA]
            Extended_used_ga.append(GA)
            # print(GA)


    # extend
    for GA in Extended_Vulnerable_dependency_from_pojs.keys():
        Extended_used_vulne_libs[GA] = []

        for V in Extended_Vulnerable_dependency_from_pojs[GA].keys():
            Extended_used_vulne_libs[GA].append( V )

            for poj in Extended_Vulnerable_dependency_from_pojs[GA][V]:
                if (poj not in affected_pojs__wangying) and (poj not in Extended_affected_pojs):
                    Extended_affected_pojs.append(poj)


    # total// 添加
    affected_pojs_total = []
    used_vulne_libs_total = []

    affected_pojs_total.extend( affected_pojs__wangying )
    affected_pojs_total.extend( Extended_affected_pojs )
    affected_pojs_total = list( set( affected_pojs_total ) )

    used_vulne_libs_total = used_vulne_libs_wangying
    for GA in Extended_used_vulne_libs:
        if GA not in used_vulne_libs_total.keys():
            used_vulne_libs_total[GA] = Extended_used_vulne_libs[GA]
        else:
            for V in Extended_used_vulne_libs[GA]:
                if V not in used_vulne_libs_total[GA]:
                    used_vulne_libs_total[GA].append(V)

    JSONFIle_processing.write(affected_pojs_total, "Wangying_FSEData/affected_pojs_total.json")
    JSONFIle_processing.write(used_vulne_libs_total, "Wangying_FSEData/used_vulne_libs_total.json")





def write():
    global Extended_used_vulne_libs, Extended_affected_pojs , Extended_Vulnerable_dependency_from_pojs, Extended_used_ga
    print("len extended affected poj:", len( Extended_affected_pojs ))
    print("len extended used ga:", len(Extended_used_ga) )
    JSONFIle_processing.write(Extended_Vulnerable_dependency_from_pojs,Extended_Vulnerable_dependency_from_pojs_path)
    JSONFIle_processing.write(Extended_affected_pojs,Extended_affected_pojs_path)
    JSONFIle_processing.write(Extended_used_vulne_libs,Extended_used_vulne_libs_path)
    JSONFIle_processing.write(Extended_used_ga, "Wangying_FSEData/Extended_used_ga.json")

if __name__ == '__main__':
    read()
    collectData()
    write()