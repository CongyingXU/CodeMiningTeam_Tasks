# -*- coding: utf-8 -*-

"""
Created on 2020-02-20 11:48  

@author: congyingxu
"""

from CommonFunction import JSONFIle_processing
from CVE.Step3_ApplyCVEData import compareVersions

# pojs dependency_data, GA 为 key
Pojs_GA_dependency_data_path = '/Users/congyingxu/Downloads/CodeMiningTeam_Tasks/GenerateDG/Dependency_Data/GAV_PojsDependency_data.json'
Pojs_GA_dependency_data = {}

CVE_GAInfo_data_path = "/Users/congyingxu/Downloads/CodeMiningTeam_Tasks/CVE/Local_Data/CVE_GAInfo.json"
CVE_GAInfo_data = {}

LocalRepoVP_CVE_Data_path = "/Users/congyingxu/Downloads/CodeMiningTeam_Tasks/CVE/Local_Data/LocalRepoVP_CVE.json"
LocalRepoVP_CVE_Data ={}

VPV_CVE_Data_path = "/Users/congyingxu/Downloads/CodeMiningTeam_Tasks/CVE/Local_Data/VulnerableVP_CVE.json"
VPV_CVE_Data = {}

Vulnerable_Pojs_GAV_dependency_data = {}
Vulnerable_Pojs_list = []

def read():
    global Pojs_GA_dependency_data, CVE_GAInfo_data , LocalRepoVP_CVE_Data, VPV_CVE_Data
    Pojs_GA_dependency_data = JSONFIle_processing.read(Pojs_GA_dependency_data_path)
    CVE_GAInfo_data = JSONFIle_processing.read(CVE_GAInfo_data_path)
    VPV_CVE_Data = JSONFIle_processing.read(VPV_CVE_Data_path)
    LocalRepoVP_CVE_Data = JSONFIle_processing.read(LocalRepoVP_CVE_Data_path)


def matchVersion(GA):
    # 返回该GA对应Version所 应用的poj list

    result_item = {}
    for used_version in Pojs_GA_dependency_data[GA]:


        # GA -> VP
        VP = CVE_GAInfo_data[GA]["VendorProduct"]
        if VP not in VPV_CVE_Data.keys():
            return result_item
        vulnerable_versionInfo_list = VPV_CVE_Data[VP].keys()
        # 该version是否是 缺陷？
        for vulnerable_versionInfo in vulnerable_versionInfo_list:

            # Version_Num:NA||versionStartIncluding:NA||versionEndIncluding:NA||versionStartExcluding:NA||versionEndExcluding:NA
            version_info_list = vulnerable_versionInfo.split('||')
            Version_Num = version_info_list[0].split(':')[1]
            versionStartIncluding = version_info_list[1].split(':')[1]
            versionEndIncluding = version_info_list[2].split(':')[1]
            versionStartExcluding = version_info_list[3].split(':')[1]
            versionEndExcluding = version_info_list[4].split(':')[1]


            # judge
            if used_version == Version_Num:
                # ??????????????????????????????????????????/ 这样写逻辑颖哥没问题吧？？？？？？
                # zhong
                result_item[used_version] = Pojs_GA_dependency_data[GA][used_version]

            elif versionStartIncluding != "NA" and compareVersions.compared_version(used_version,versionStartIncluding) > -1 :
                if versionEndIncluding != "NA" and compareVersions.compared_version(used_version,versionEndIncluding) < 1:
                    #zhong
                    # ??????????????????????????????????????????/ 这样写逻辑颖哥没问题吧？？？？？？
                    # zhong
                    result_item[used_version] = Pojs_GA_dependency_data[GA][used_version]

            elif versionStartExcluding != "NA" and compareVersions.compared_version(used_version,versionStartIncluding) == 1 :
                if versionEndExcluding != "NA" and compareVersions.compared_version(used_version,
                                                                                    versionEndExcluding) == -1:
                    # zhong
                    # ??????????????????????????????????????????/ 这样写逻辑颖哥没问题吧？？？？？？
                    # zhong
                    result_item[used_version] = Pojs_GA_dependency_data[GA][used_version]

    return result_item



def collect():
    global Vulnerable_Pojs_GA_dependency_data
    for GA in Pojs_GA_dependency_data.keys():
        if GA in CVE_GAInfo_data.keys():# GA 是有缺陷的

            # matchVersion
            matchVersion_result = matchVersion(GA)
            # print(matchVersion_result)
            if len(matchVersion_result) > 0:
                Vulnerable_Pojs_GAV_dependency_data[GA] = matchVersion(GA)
            # print(GA)
            # Vulnerable_Pojs_GA_dependency_data[GA] = Pojs_GA_dependency_data[GA]


def write():
    global Vulnerable_Pojs_list
    JSONFIle_processing.write(Vulnerable_Pojs_GAV_dependency_data, "Vulnerable_dependency_fromPojs.json")

    count_GAVs = 0
    count_poj = 0
    for GA in Vulnerable_Pojs_GAV_dependency_data.keys():
        count_GAVs += len(Vulnerable_Pojs_GAV_dependency_data[GA].keys())
        for V in Vulnerable_Pojs_GAV_dependency_data[GA].keys():
            # count_poj += len( Vulnerable_Pojs_GAV_dependency_data[GA][V] )
            Vulnerable_Pojs_list.extend( Vulnerable_Pojs_GAV_dependency_data[GA][V] )

    Vulnerable_Pojs_list = set( Vulnerable_Pojs_list )

    print("count GAVs: ", count_GAVs)
    print("count pojs：", len(Vulnerable_Pojs_list))

if __name__ == '__main__':
    read()
    collect()
    write()

