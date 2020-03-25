# -*- coding: utf-8 -*-

"""
Created on 2020-02-25 23:27  

@author: congyingxu
"""

from CommonFunction import JSONFIle_processing
from CVE_FSE.Step3_ApplyCVEData import compareVersions
import semver

All_used_vule_ga_path = "Wangying_FSEData/vulnerable_lib_for_githubissue.json"
All_used_vule_ga = []

ga_all_version_path = "Wangying_FSEData/lib_versions_new_forgithubissue.json"
ga_all_version = {}

candidate_safe_gav_path = "Wangying_FSEData/candidate_safe_gav_for_githubissue.json"
candidate_safe_gav = {}

def read():
    global All_used_vule_ga, ga_all_version, candidate_safe_gav

    All_used_vule_ga = JSONFIle_processing.read(All_used_vule_ga_path)
    ga_all_version = JSONFIle_processing.read(ga_all_version_path)
    pass

def collectData():
    global candidate_safe_gav

    for ele in ga_all_version:
        # print( ele)
        GA = ele["lib"][:-14]
        GA = ele["lib"].split("__fdse__")[0] + "__fdse__" + ele["lib"].split("__fdse__")[1]
        versions = ele["versions"]

        # if GA == 'commons-beanutils__fdse__commons-beanutils':


        if GA in All_used_vule_ga.keys():
            for used_version in All_used_vule_ga[GA]:
                GAV_str = GA + "__fdse__" + used_version
                if GAV_str not in candidate_safe_gav.keys():
                    candidate_safe_gav[GAV_str] =[]
                for candidate_version in versions:
                    if candidate_version not in All_used_vule_ga[GA] and compareVersion(candidate_version,used_version) == 1:
                        candidate_safe_gav[GAV_str].append(candidate_version)



    for GA in All_used_vule_ga.keys():
        if GA not in candidate_safe_gav.keys():
            print("GA not in:", GA)
    pass

def compareVersion(ver1, ver2):
    try:
        compare_result = semver.compare(ver1, ver2)
    except:
        compare_result = compareVersions.compared_version(ver1, ver2)

    return compare_result


def IsLaterVersion(ver1,verlist):
    for ver2 in verlist:
        try:
            compare_result = semver.compare(ver1,ver2)
        except:
            compare_result = compareVersions.compared_version(ver1,ver2)

        if compare_result < 1:
            return False

    return True

def sortversions(verlist):

    if len(verlist) < 2:
        return verlist
    result_list  = [verlist[0]]

    for ver in verlist[1:]:

        for i in range(len( result_list )):
            in_ver = result_list[i]
            try:
                compare_result = semver.compare(ver,in_ver)
            except:
                compare_result = compareVersions.compared_version(ver,in_ver)

            if compare_result>-1:
                result_list.insert(i+1, ver)

    print("verlist",verlist)
    print(result_list)
    return result_list

def write():
    global All_used_vule_ga, ga_all_version, candidate_safe_gav

    JSONFIle_processing.write(candidate_safe_gav,candidate_safe_gav_path)


if __name__ == '__main__':
    read()
    collectData()
    write()