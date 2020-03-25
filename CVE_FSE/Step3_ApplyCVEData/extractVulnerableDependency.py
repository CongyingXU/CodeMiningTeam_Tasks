# -*- coding: utf-8 -*-

"""
Created on 2020-02-20 11:48  

@author: congyingxu
"""

from CommonFunction import JSONFIle_processing
from CVE_FSE.Step3_ApplyCVEData import compareVersions

# pojs dependency_data, GA 为 key
Pojs_GA_dependency_data_path = '/Users/congyingxu/Downloads/CodeMiningTeam_Tasks/GenerateDG/Dependency_Data/GAV_PojsDependency_data.json'
Pojs_GA_dependency_data = {}

CVE_GAInfo_data_path = "/Users/congyingxu/Downloads/CodeMiningTeam_Tasks/CVE_FSE/Local_Data/CVE_GAInfo.json"
CVE_GAInfo_data = {}

LocalRepoVP_CVE_Data_path = "/Users/congyingxu/Downloads/CodeMiningTeam_Tasks/CVE_FSE/Local_Data/LocalRepoVP_CVE.json"
LocalRepoVP_CVE_Data ={}

VPV_CVE_Data_path = "/Users/congyingxu/Downloads/CodeMiningTeam_Tasks/CVE_FSE/Local_Data/VulnerableVP_CVE.json"
VPV_CVE_Data = {}

Vulnerable_Pojs_GAV_dependency_data = {}
Vulnerable_Pojs_list = []

GAV_CVE_BuggyMethod_path = "Wangying_FSEData/GAV_CVE_BuggyMethod.json"
GAV_CVE_BuggyMethod = []

vulne_lib_poj_path = "Wangying_FSEData/vulne_lib_poj.json"
vulne_lib_poj = []

UsedGAV_CVE_mapping_Congying_path = "Wangying_FSEData/UsedGAV_CVE_mapping_Congying.json"
UsedGAV_CVE_mapping_Congying = {}


Invalid_VPV = set()

def read():
    global Pojs_GA_dependency_data, CVE_GAInfo_data , LocalRepoVP_CVE_Data, VPV_CVE_Data, GAV_CVE_BuggyMethod, vulne_lib_poj
    Pojs_GA_dependency_data = JSONFIle_processing.read(Pojs_GA_dependency_data_path)
    CVE_GAInfo_data = JSONFIle_processing.read(CVE_GAInfo_data_path)
    VPV_CVE_Data = JSONFIle_processing.read(VPV_CVE_Data_path)
    LocalRepoVP_CVE_Data = JSONFIle_processing.read(LocalRepoVP_CVE_Data_path)
    GAV_CVE_BuggyMethod = JSONFIle_processing.read(GAV_CVE_BuggyMethod_path)
    vulne_lib_poj = JSONFIle_processing.read(vulne_lib_poj_path)


def matchVersion(GA):
    global  Invalid_VPV, GAV_CVE_BuggyMethod, vulne_lib_poj, UsedGAV_CVE_mapping_Congying
    # 返回该GA对应Version所 应用的poj list

    result_item = {}
    for used_version in Pojs_GA_dependency_data[GA]:
        if len(used_version) == 0 or 'snapshot' in used_version.lower():
            continue
        GAV_str = GA + '__fdse__' + used_version

        # GA -> VP
        VP = CVE_GAInfo_data[GA]["VendorProduct"]
        if VP not in VPV_CVE_Data.keys():
            return result_item
        vulnerable_versionInfo_list = VPV_CVE_Data[VP].keys()
        # 该version是否是 缺陷？
        touch_onlyoneNA = 0
        for vulnerable_versionInfo in vulnerable_versionInfo_list:

            # Version_Num:NA||versionStartIncluding:NA||versionEndIncluding:NA||versionStartExcluding:NA||versionEndExcluding:NA
            version_info_list = vulnerable_versionInfo.split('||')
            Version_Num = version_info_list[0].split(':')[1]
            versionStartIncluding = version_info_list[1].split(':')[1]
            versionEndIncluding = version_info_list[2].split(':')[1]
            versionStartExcluding = version_info_list[3].split(':')[1]
            versionEndExcluding = version_info_list[4].split(':')[1]

            # if Version_Num != "NA" and (versionStartIncluding!='NA' or versionEndIncluding!='NA' or versionStartExcluding!='NA' or versionEndExcluding !='NA'):
            # print(Version_Num, versionStartIncluding,versionEndIncluding,versionStartExcluding,versionEndExcluding)



            # judge
            # break or continue
            if len(used_version) == 0 or used_version[0] == '[' or used_version[0]=='$' or used_version[-1]=='}':
                break

            if Version_Num !='NA':
                if used_version == Version_Num:
                    result_item[used_version] = Pojs_GA_dependency_data[GA][used_version]
            else: # Version_Num =='NA'

                if versionStartIncluding != "NA" and compareVersions.compared_version(used_version,versionStartIncluding) > -1:

                    if (versionEndIncluding != "NA" and compareVersions.compared_version(used_version,versionEndIncluding) < 1)\
                            or ( versionEndExcluding != "NA" and compareVersions.compared_version(used_version,versionEndExcluding) == -1):
                        # print(used_version, versionStartIncluding, versionEndIncluding, versionStartExcluding, versionEndExcluding)

                        result_item[used_version] = Pojs_GA_dependency_data[GA][used_version]

                        #补充数据
                        if GAV_str in UsedGAV_CVE_mapping_Congying.keys():
                            UsedGAV_CVE_mapping_Congying[GAV_str].extend(VPV_CVE_Data[VP][vulnerable_versionInfo])
                            UsedGAV_CVE_mapping_Congying[GAV_str] = list(set(UsedGAV_CVE_mapping_Congying[GAV_str]))
                        else:
                            UsedGAV_CVE_mapping_Congying[GAV_str] =  VPV_CVE_Data[VP][vulnerable_versionInfo]

                        break

                    # find special
                    if versionEndIncluding == "NA" and versionEndExcluding == 'NA':
                        # print(VP,GA,vulnerable_versionInfo)
                        touch_onlyoneNA = 1
                        # break

                elif versionStartIncluding == "NA":

                    if versionStartExcluding != "NA" and compareVersions.compared_version(used_version,versionStartExcluding) == 1:

                        if ( versionEndExcluding != "NA" and compareVersions.compared_version(used_version,versionEndExcluding) == -1) \
                                or ( versionEndIncluding != "NA" and compareVersions.compared_version(used_version,versionEndIncluding)< 1) :
                            # print(used_version, versionStartIncluding, versionEndIncluding, versionStartExcluding, versionEndExcluding)
                            result_item[used_version] = Pojs_GA_dependency_data[GA][used_version]
                            # 补充数据
                            if GAV_str in UsedGAV_CVE_mapping_Congying.keys():
                                UsedGAV_CVE_mapping_Congying[GAV_str].extend(VPV_CVE_Data[VP][vulnerable_versionInfo])
                                UsedGAV_CVE_mapping_Congying[GAV_str] = list(
                                    set(UsedGAV_CVE_mapping_Congying[GAV_str]))
                            else:
                                UsedGAV_CVE_mapping_Congying[GAV_str] = VPV_CVE_Data[VP][vulnerable_versionInfo]
                            break

                            # find special
                        if versionEndExcluding == "NA" and versionEndIncluding == "NA":
                            # print(VP,GA,vulnerable_versionInfo)
                            touch_onlyoneNA = 1
                            # break

                    elif versionStartExcluding == "NA":

                        # find special
                        if  (versionEndExcluding != "NA" and compareVersions.compared_version(used_version,versionEndExcluding) == -1) \
                                or ( versionEndIncluding != "NA" and compareVersions.compared_version(used_version,versionEndIncluding)< 1) :


                            # result_item[used_version] = Pojs_GA_dependency_data[GA][used_version]
                            # break

                            touch_onlyoneNA = 1
                            # print(VP,GA,vulnerable_versionInfo)
                            # break
                        # 2.0.0-alpha4 2.1.0 2.1.3 NA NA

         # 碰到我这里的禁区了，用颖姐的数据试试康？
        if touch_onlyoneNA == 1 and len(result_item) == 0 :
            # print(VP, GA, used_version)

            GAV_str =  GA + "__fdse__" + used_version

            # if GAV_str in GAV_CVE_BuggyMethod.keys():
            #     result_item[used_version] = Pojs_GA_dependency_data[GA][used_version]
            if GA in vulne_lib_poj.keys() and used_version in vulne_lib_poj[GA]:
                result_item[used_version] = Pojs_GA_dependency_data[GA][used_version]
            elif used_version[-1]!='@':
                # print(GA + "__fdse__" + used_version)
                Invalid_VPV.add(GA + "__fdse__" + used_version)

                # result_item[used_version] = Pojs_GA_dependency_data[GA][used_version]

                # Invalid_VPV.add(GA)
            # result_item[used_version] = Pojs_GA_dependency_data[GA][used_version]



    return result_item



def collect():
    global Vulnerable_Pojs_GA_dependency_data
    for GA in Pojs_GA_dependency_data.keys():
        if GA in CVE_GAInfo_data.keys():# GA 是有缺陷的

            # matchVersion
            matchVersion_result = matchVersion(GA)
            # print(matchVersion_result)
            if len(matchVersion_result) > 0:
                Vulnerable_Pojs_GAV_dependency_data[GA] = matchVersion_result
            # print(GA)
            # Vulnerable_Pojs_GA_dependency_data[GA] = Pojs_GA_dependency_data[GA]

    print(len(Invalid_VPV))


def write():
    global Vulnerable_Pojs_list, UsedGAV_CVE_mapping_Congying
    JSONFIle_processing.write(Vulnerable_Pojs_GAV_dependency_data, "Vulnerable_dependency_fromPojs.json")
    JSONFIle_processing.write(UsedGAV_CVE_mapping_Congying, UsedGAV_CVE_mapping_Congying_path)

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

