# -*- coding: utf-8 -*-

"""
Created on 2020-02-26 20:34  

@author: congyingxu

生成：用于发issue的粗粒度GAV信息
"""
from CommonFunction import JSONFIle_processing



proj_vulne_lib_info_path = "Wangying_FSEData/proj_vulne_lib_info.json"
proj_vulne_lib_info_completed_path = "Wangying_FSEData/proj_vulne_lib_info_completed.json"
proj_vulne_lib_info = {}
Pojs_GAV_Path_path = "Wangying_FSEData/Pojs_GAV_Path.json"
Pojs_GAV_Path = {}
candidate_safe_gav_for_githubissue_path = "Wangying_FSEData/candidate_safe_gav_for_githubissue.json"
candidate_safe_gav_for_githubissue = {}


def read():
    global proj_vulne_lib_info, Pojs_GAV_Path, candidate_safe_gav_for_githubissue
    proj_vulne_lib_info = JSONFIle_processing.read(proj_vulne_lib_info_path)
    Pojs_GAV_Path = JSONFIle_processing.read(Pojs_GAV_Path_path)
    candidate_safe_gav_for_githubissue = JSONFIle_processing.read(candidate_safe_gav_for_githubissue_path)
    pass

def collectData():
    for poj in proj_vulne_lib_info.keys():
        for GA in proj_vulne_lib_info[poj].keys():
            for version in proj_vulne_lib_info[poj][GA].keys():
                pass
                GAV_str = GA +"__fdse__"+version
                path = Pojs_GAV_Path[poj][GA+version]
                cve =  proj_vulne_lib_info[poj][GA][version]
                safeVersion = candidate_safe_gav_for_githubissue[GAV_str]

                proj_vulne_lib_info[poj][GA][version] = { "path":path, "cve":cve, "safeVersion":safeVersion }




def write():
    JSONFIle_processing.write(proj_vulne_lib_info,proj_vulne_lib_info_completed_path)


if __name__ == '__main__':
    read()
    collectData()
    write()