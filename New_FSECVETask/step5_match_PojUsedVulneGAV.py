# -*- coding: utf-8 -*-

"""
Created on 2020-02-26 17:25  

@author: congyingxu
match_PojUsedVulneGAV
匹配上：poj使用的有缺陷的GAV


all used gav: 18041
length D5_Vulne_SpecificGAv_UsedByPojs gav:  21
length D5_Vulne_WholeRangeGAv_UsedByPojs gav:  148
length D5_Vulne_PartRangeGAv_UsedByPojs gav:  216

length D5_Vulne_SpecificGAv_UsedByPojs_pojset :  11
length D5_Vulne_WholeRangeGAv_UsedByPojs_pojset :  50
length D5_Vulne_PartRangeGAv_UsedByPojs_pojset gav:  91

"""

from CommonFunction import JSONFIle_processing
from New_FSECVETask import step3_generate_SpecificGAV_CVE,compareVersions


D3_SpecificGAv_CVE = JSONFIle_processing.read( step3_generate_SpecificGAV_CVE.D3_SpecificGAv_CVE_path)
D3_WholeRangeGAv_CVE = JSONFIle_processing.read( step3_generate_SpecificGAV_CVE.D3_WholeRangeGAv_CVE_path)
D3_PartRangeGAv_CVE = JSONFIle_processing.read( step3_generate_SpecificGAV_CVE.D3_PartRangeGAv_CVE_path)


D5_Vulne_SpecificGAv_UsedByPojs_path = "Data/D5_Vulne_SpecificGAv_UsedByPojs.json"
D5_Vulne_SpecificGAv_UsedByPojs = {}

D5_Vulne_WholeRangeGAv_UsedByPojs_path = "Data/D5_Vulne_WholeRangeGAv_UsedByPojs.json"
D5_Vulne_WholeRangeGAv_UsedByPojs = {}

D5_Vulne_PartRangeGAv_UsedByPojs_path = "Data/D5_Vulne_PartRangeGAv_UsedByPojs.json"
D5_Vulne_PartRangeGAv_UsedByPojs = {}


GAV_PojsDependency_data_path = "Pre-Data/GAV_PojsDependency_data.json"
GAV_PojsDependency_data = {}

def read():
    global GAV_PojsDependency_data
    GAV_PojsDependency_data = JSONFIle_processing.read( GAV_PojsDependency_data_path )

def match_PojUsedVulneGAV():
    global GAV_PojsDependency_data, D5_Vulne_SpecificGAv_UsedByPojs, D5_Vulne_WholeRangeGAv_UsedByPojs,D5_Vulne_PartRangeGAv_UsedByPojs

    used_GAV_count = 0
    used_vulne_GAV_count = 0
    for poj_used_GA in GAV_PojsDependency_data.keys():
        for poj_used_version in GAV_PojsDependency_data[poj_used_GA].keys():
            if len(poj_used_version) == 0 or 'snapshot' in poj_used_version.lower() or poj_used_version[0] == '[' or poj_used_version[0]=='$' or poj_used_version[-1]=='}':
                continue

            # 项目使用的GAV，
            GAV_str = poj_used_GA + "__fdse__" + poj_used_version
            used_GAV_count +=1


            # D3_SpecificGAv_CVE
            if poj_used_GA in D3_SpecificGAv_CVE.keys():
                if poj_used_version in D3_SpecificGAv_CVE[poj_used_GA].keys():
                    #zhong
                    if GAV_str not in D5_Vulne_PartRangeGAv_UsedByPojs.keys():
                        D5_Vulne_SpecificGAv_UsedByPojs[GAV_str] = GAV_PojsDependency_data[poj_used_GA][poj_used_version]
                        used_vulne_GAV_count +=1
                        continue
                    else:
                        print("Bu Ying Dang")


            # D3_WholeRangeGAv_CVE
            if poj_used_GA in D3_WholeRangeGAv_CVE.keys():
                for rangeversion_info in D3_WholeRangeGAv_CVE[poj_used_GA].keys():
                    version_info_list = rangeversion_info.split('||')
                    Version_Num = version_info_list[0].split(':')[1]
                    versionStartIncluding = version_info_list[1].split(':')[1]
                    versionEndIncluding = version_info_list[2].split(':')[1]
                    versionStartExcluding = version_info_list[3].split(':')[1]
                    versionEndExcluding = version_info_list[4].split(':')[1]

                    if versionStartIncluding != "NA" and compareVersions.compared_version(poj_used_version,versionStartIncluding) > -1:
                        if (versionEndIncluding != "NA" and compareVersions.compared_version(poj_used_version,versionEndIncluding) < 1) \
                                or (versionEndExcluding != "NA" and compareVersions.compared_version(poj_used_version,versionEndExcluding) == -1):
                            #zhong
                            if GAV_str not in D5_Vulne_WholeRangeGAv_UsedByPojs.keys():
                                D5_Vulne_WholeRangeGAv_UsedByPojs[GAV_str] = GAV_PojsDependency_data[poj_used_GA][poj_used_version]
                                used_vulne_GAV_count += 1
                                continue

                    if versionStartExcluding != "NA" and compareVersions.compared_version(poj_used_version,versionStartExcluding) == 1:
                        if (versionEndExcluding != "NA" and compareVersions.compared_version(poj_used_version,versionEndExcluding) == -1) \
                                or (versionEndIncluding != "NA" and compareVersions.compared_version(poj_used_version,versionEndIncluding) < 1):
                            # zhong
                            if GAV_str not in D5_Vulne_WholeRangeGAv_UsedByPojs.keys():
                                D5_Vulne_WholeRangeGAv_UsedByPojs[GAV_str] = GAV_PojsDependency_data[poj_used_GA][
                                    poj_used_version]
                                used_vulne_GAV_count += 1
                                continue

            # D3_PartRangeGAv_CVE
            if poj_used_GA in D3_PartRangeGAv_CVE.keys():
                for rangeversion_info in D3_PartRangeGAv_CVE[poj_used_GA].keys():
                    version_info_list = rangeversion_info.split('||')
                    Version_Num = version_info_list[0].split(':')[1]
                    versionStartIncluding = version_info_list[1].split(':')[1]
                    versionEndIncluding = version_info_list[2].split(':')[1]
                    versionStartExcluding = version_info_list[3].split(':')[1]
                    versionEndExcluding = version_info_list[4].split(':')[1]

                    if versionStartIncluding != "NA" and compareVersions.compared_version(poj_used_version,versionStartIncluding) > -1:
                        if versionEndIncluding == "NA" or versionEndExcluding == 'NA':
                            # zhong
                            if GAV_str not in D5_Vulne_PartRangeGAv_UsedByPojs.keys():
                                D5_Vulne_PartRangeGAv_UsedByPojs[GAV_str] = GAV_PojsDependency_data[poj_used_GA][poj_used_version]
                                used_vulne_GAV_count += 1
                                continue
                    elif versionStartIncluding == "NA":
                        if versionStartExcluding != "NA" and compareVersions.compared_version(poj_used_version, versionStartExcluding) == 1:
                            if versionEndExcluding == "NA" and versionEndIncluding == "NA":
                                # zhong
                                if GAV_str not in D5_Vulne_PartRangeGAv_UsedByPojs.keys():
                                    D5_Vulne_PartRangeGAv_UsedByPojs[GAV_str] = GAV_PojsDependency_data[poj_used_GA][poj_used_version]
                                    used_vulne_GAV_count += 1
                                    continue
                        elif versionStartExcluding == "NA":

                            if (versionEndExcluding != "NA" and compareVersions.compared_version(poj_used_version,versionEndExcluding) == -1) \
                                    or (versionEndIncluding != "NA" and compareVersions.compared_version(poj_used_version,versionEndIncluding) < 1):
                                # zhong
                                if GAV_str not in D5_Vulne_PartRangeGAv_UsedByPojs.keys():
                                    D5_Vulne_PartRangeGAv_UsedByPojs[GAV_str] = GAV_PojsDependency_data[poj_used_GA][poj_used_version]
                                    used_vulne_GAV_count += 1
                                    continue

            else:
                pass

            pass
    pass

    print("all used gav:", used_GAV_count)
    print("used_vulne_GAV_count:",used_vulne_GAV_count)

def write():
    global GAV_PojsDependency_data, D5_Vulne_SpecificGAv_UsedByPojs, D5_Vulne_WholeRangeGAv_UsedByPojs,D5_Vulne_PartRangeGAv_UsedByPojs

    JSONFIle_processing.write(D5_Vulne_SpecificGAv_UsedByPojs, D5_Vulne_SpecificGAv_UsedByPojs_path)
    JSONFIle_processing.write(D5_Vulne_WholeRangeGAv_UsedByPojs, D5_Vulne_WholeRangeGAv_UsedByPojs_path)
    JSONFIle_processing.write(D5_Vulne_PartRangeGAv_UsedByPojs, D5_Vulne_PartRangeGAv_UsedByPojs_path)



    D5_Vulne_SpecificGAv_UsedByPojs_pojset = []
    for GAV_str in D5_Vulne_SpecificGAv_UsedByPojs.keys():
        D5_Vulne_SpecificGAv_UsedByPojs_pojset.extend( D5_Vulne_SpecificGAv_UsedByPojs[GAV_str] )
    D5_Vulne_SpecificGAv_UsedByPojs_pojset = list( set( D5_Vulne_SpecificGAv_UsedByPojs_pojset ) )

    D5_Vulne_WholeRangeGAv_UsedByPojs_pojset = []
    for GAV_str in D5_Vulne_WholeRangeGAv_UsedByPojs.keys():
        D5_Vulne_WholeRangeGAv_UsedByPojs_pojset.extend(D5_Vulne_WholeRangeGAv_UsedByPojs[GAV_str])
    D5_Vulne_WholeRangeGAv_UsedByPojs_pojset = list(set(D5_Vulne_WholeRangeGAv_UsedByPojs_pojset))

    D5_Vulne_PartRangeGAv_UsedByPojs_pojset = []
    for GAV_str in D5_Vulne_PartRangeGAv_UsedByPojs.keys():
        D5_Vulne_PartRangeGAv_UsedByPojs_pojset.extend(D5_Vulne_PartRangeGAv_UsedByPojs[GAV_str])
    D5_Vulne_PartRangeGAv_UsedByPojs_pojset = list(set(D5_Vulne_PartRangeGAv_UsedByPojs_pojset))

    print("length D5_Vulne_SpecificGAv_UsedByPojs gav: ",len(D5_Vulne_SpecificGAv_UsedByPojs.keys()))
    print("length D5_Vulne_WholeRangeGAv_UsedByPojs gav: ", len(D5_Vulne_WholeRangeGAv_UsedByPojs.keys()))
    print("length D5_Vulne_PartRangeGAv_UsedByPojs gav: ", len(D5_Vulne_PartRangeGAv_UsedByPojs.keys()))

    print("length D5_Vulne_SpecificGAv_UsedByPojs_pojset : ", len(D5_Vulne_SpecificGAv_UsedByPojs_pojset))
    print("length D5_Vulne_WholeRangeGAv_UsedByPojs_pojset : ", len(D5_Vulne_WholeRangeGAv_UsedByPojs_pojset))
    print("length D5_Vulne_PartRangeGAv_UsedByPojs_pojset gav: ", len(D5_Vulne_PartRangeGAv_UsedByPojs_pojset))

    vuln_pojs_set = []
    vuln_pojs_set.extend(D5_Vulne_SpecificGAv_UsedByPojs_pojset  )
    vuln_pojs_set.extend(D5_Vulne_WholeRangeGAv_UsedByPojs_pojset)
    vuln_pojs_set.extend(D5_Vulne_PartRangeGAv_UsedByPojs_pojset)

    vuln_pojs_set = set( vuln_pojs_set )
    print("length vuln_pojs_set:",len(vuln_pojs_set))


if __name__ == '__main__':
    read()
    match_PojUsedVulneGAV()
    write()

