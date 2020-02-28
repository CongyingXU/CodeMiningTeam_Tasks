# -*- coding: utf-8 -*-

"""
Created on 2020-02-28 10:06  

@author: congyingxu

生成vulner GAV + nearest safe GAV, 且jar包可寻
"""
import sys
sys.path.append('../')
sys.path.append('../../')

import semver
from CommonFunction import File_processing, JSONFIle_processing
from CVE.Step3_ApplyCVEData import compareVersions

candidate_safe_gav_path = "Wangying_FSEData/candidate_safe_gav_for_githubissue.json"
candidate_safe_gav = JSONFIle_processing.read( candidate_safe_gav_path )

jar_repo_path = "/Users/congyingxu/Downloads/CrawledGAVs_0218/"
gav_pair = {}
map_GAV_GAVmd5 = {}

not_existing_ga_v = {}
def generatepair():

    global gav_pair, map_GAV_GAVmd5

    GAmd5_list  = File_processing.walk_L1_Folders( jar_repo_path )
    for gavmd5 in GAmd5_list:
        if len( gavmd5.split( "__fdse__" ) ) > 2:
            ga = gavmd5.split( "__fdse__" )[0] + "__fdse__" + gavmd5.split( "__fdse__" )[1]
            map_GAV_GAVmd5[ga] = gavmd5


    for gav in candidate_safe_gav.keys():
        ga = gav.split("__fdse__")[0] +"__fdse__"+ gav.split("__fdse__")[1]
        v = gav.split("__fdse__")[2]

        if jarExisting(ga,v) and len( candidate_safe_gav[gav] )>0:
            nearst_version = get_nearst_version(ga,v,candidate_safe_gav[gav])
            if nearst_version != '':
                gav_pair[gav] = nearst_version




        else:
            continue

def get_nearst_version(ga,v,original_ver_list):
    if len(original_ver_list) <2 :
        print(ga,v,original_ver_list)
        return original_ver_list[0]


    index = 0
    result_version = ''

    for index in range( len(original_ver_list) ):
        if jarExisting(ga, original_ver_list[index]):
            result_version = original_ver_list[index]

    if result_version != '' and index< len(original_ver_list)-1:
        for ver in original_ver_list[index+1:]:

            # compare version
            try:
                compare_result = semver.compare(result_version,ver)
            except:
                compare_result = compareVersions.compared_version(result_version,ver)

            if compare_result == 1 and jarExisting(ga,ver):
                result_version = ver

    return  result_version





def jarExisting(GA,version):
    global not_existing_ga_v
    if GA not in map_GAV_GAVmd5.keys():
        return False
    gavmd5 = map_GAV_GAVmd5[GA]
    jar_name = GA.split("__fdse__")[1] + '-' + version +'.jar'
    jar_path = jar_repo_path + gavmd5 +'/'+version +'/' + jar_name

    if File_processing.pathExist(jar_path):
        return True
    else:
        if GA not in not_existing_ga_v.keys():
            not_existing_ga_v[GA] = [version]
        else:
            not_existing_ga_v[GA].append(version)
        # print("jar not Existing, ", jar_path)
        return False


def write():
    global gav_pair, not_existing_ga_v
    JSONFIle_processing.write(gav_pair, "Wangying_FSEData/gav_rec_pair.json")
    JSONFIle_processing.write(not_existing_ga_v,"Wangying_FSEData/not_existing_ga_v.json")


if __name__ == '__main__':
    generatepair()
    write()