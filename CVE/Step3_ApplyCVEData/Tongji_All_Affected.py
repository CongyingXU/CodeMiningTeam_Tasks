# -*- coding: utf-8 -*-

"""
Created on 2020-02-25 15:21  

@author: congyingxu

用于统计 当前实验对象的相关数据
哪些项目，用了哪些GAV，触发了哪些CVE？

最多的，最少的项目是？平均是？中位数是？上下4分位数是？
"""

from CommonFunction import JSONFIle_processing

All_affected_pojs_path = "Wangying_FSEData/affected_projs_total.json"
All_used_vule_ga_path = "Wangying_FSEData/used_vulne_libs_total.json"
GAV_CVE_Buggymethod_wangying_path = "Wangying_FSEData/GAV_CVE_BuggyMethod.json"
Pojs_GAVDependency_data_path = "Wangying_FSEData/Pojs_GAVDependency_data.json"

All_related_CVE_path = "Wangying_FSEData/All_related_CVE.json"
All_AffectedPojModule_UsedVulnerGAV_RelatedCVE_path = "Wangying_FSEData/All_AffectedPojModule_UsedVulnerGAV_RelatedCVE.json"

UsedGAV_CVE_mapping_Congying_path = "Wangying_FSEData/UsedGAV_CVE_mapping_Congying.json"
UsedGAV_CVE_mapping_Congying = {}

All_affected_pojs = []
All_used_vule_ga = []
GAV_CVE_Buggymethod_wangying = {}
All_related_CVE = []

All_AffectedPojModule_UsedVulnerGAV_RelatedCVE = {}

def read():
    global All_affected_pojs, All_used_vule_ga, GAV_CVE_Buggymethod_wangying, Pojs_GAVDependency_data, UsedGAV_CVE_mapping_Congying

    GAV_CVE_Buggymethod_wangying = JSONFIle_processing.read(GAV_CVE_Buggymethod_wangying_path)
    All_affected_pojs = JSONFIle_processing.read(All_affected_pojs_path)
    All_used_vule_ga = JSONFIle_processing.read(All_used_vule_ga_path)
    Pojs_GAVDependency_data = JSONFIle_processing.read(Pojs_GAVDependency_data_path)
    UsedGAV_CVE_mapping_Congying = JSONFIle_processing.read(UsedGAV_CVE_mapping_Congying_path)




def collectData():
    global All_affected_pojs, All_used_vule_ga, GAV_CVE_Buggymethod_wangying, All_AffectedPojModule_UsedVulnerGAV_RelatedCVE, Pojs_GAVDependency_data, All_related_CVE
    # 汇合


    # 计算
    for poj in All_affected_pojs:
        GAVs = Pojs_GAVDependency_data[poj]
        All_AffectedPojModule_UsedVulnerGAV_RelatedCVE[poj] = {}

        for GAV_item in GAVs:
            groupId = GAV_item["groupId"]
            artifactId = GAV_item["artifactId"]
            version = GAV_item["version"]
            poj_module = GAV_item["module"]

            GA_str = groupId + "__fdse__" + artifactId
            GAV_str = groupId + "__fdse__" + artifactId  + "__fdse__" + version
            if GA_str in All_used_vule_ga.keys() and version in All_used_vule_ga[GA_str]:
                if GAV_str in GAV_CVE_Buggymethod_wangying.keys():
                    if poj_module not in All_AffectedPojModule_UsedVulnerGAV_RelatedCVE[poj].keys():
                        All_AffectedPojModule_UsedVulnerGAV_RelatedCVE[poj][poj_module] = {GAV_str: list(GAV_CVE_Buggymethod_wangying[GAV_str].keys())}
                    else:
                        All_AffectedPojModule_UsedVulnerGAV_RelatedCVE[poj][poj_module][GAV_str] = list(GAV_CVE_Buggymethod_wangying[GAV_str].keys())
                    All_related_CVE.extend(GAV_CVE_Buggymethod_wangying[GAV_str].keys())
                elif GAV_str in UsedGAV_CVE_mapping_Congying.keys():
                    if poj_module not in All_AffectedPojModule_UsedVulnerGAV_RelatedCVE[poj].keys():
                        All_AffectedPojModule_UsedVulnerGAV_RelatedCVE[poj][poj_module] = {GAV_str: [ele.split("CVE-")[1] for ele in UsedGAV_CVE_mapping_Congying[GAV_str]]}
                    else:
                        All_AffectedPojModule_UsedVulnerGAV_RelatedCVE[poj][poj_module][GAV_str] = [ele.split("CVE-")[1] for ele in UsedGAV_CVE_mapping_Congying[GAV_str]]
                    All_related_CVE.extend(UsedGAV_CVE_mapping_Congying[GAV_str])
                else:
                    print(GAV_str,"BU YING DANG!!!")



    All_related_CVE = list( set( All_related_CVE ) )



def write():
    global All_affected_pojs, All_used_vule_ga, GAV_CVE_Buggymethod_wangying, All_AffectedPojModule_UsedVulnerGAV_RelatedCVE, Pojs_GAVDependency_data


    MetaData = {"All_affected_pojs_num": len(All_affected_pojs),
                "All_used_vule_ga_num": len(All_used_vule_ga.keys()),
                "All_related_CVE_num": len(All_related_CVE)}

    JSONFIle_processing.write(All_AffectedPojModule_UsedVulnerGAV_RelatedCVE, All_AffectedPojModule_UsedVulnerGAV_RelatedCVE_path)
    JSONFIle_processing.write( All_related_CVE,All_related_CVE_path)
    JSONFIle_processing.write( MetaData,"Wangying_FSEData/MetaData.json")


def tiaozhengshuju():

    proj_vulne_lib = JSONFIle_processing.read( "Wangying_FSEData/proj_vulne_lib.json" )
    vulne_lib_poj = {}
    for poj in proj_vulne_lib.keys():
        for GA in proj_vulne_lib[poj]:
            if GA not in vulne_lib_poj.keys():
                vulne_lib_poj[GA] = {}
            for V in proj_vulne_lib[poj][GA]:
                if V not in vulne_lib_poj[GA].keys():
                    vulne_lib_poj[GA][V] = []
                else:
                    if poj not in vulne_lib_poj[GA][V]:
                        vulne_lib_poj[GA][V].append( poj )

    JSONFIle_processing.write(vulne_lib_poj, "Wangying_FSEData/vulne_lib_poj.json")

# tiaozhengshuju()
if __name__ == '__main__':
    read()
    collectData()
    write()