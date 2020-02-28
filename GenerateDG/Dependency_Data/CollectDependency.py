# -*- coding: utf-8 -*-

"""
Created on 2020-02-20 11:01  

@author: congyingxu
"""
from CommonFunction import JSONFIle_processing, File_processing

dependency_data_path = 'total_with_path/'
dependency_data_file_list = []

Pojs_dependency_data = {}
GA_dependency_data = {}
Pojs_GAV_Path = {}


def getFileList():
    global dependency_data_file_list
    dependency_data_file_list =  File_processing.walk_L1_FileNames(dependency_data_path )



def collectDependency(file_name):
    global Pojs_GAV_Path
    file_path = dependency_data_path + file_name
    dependency_content = JSONFIle_processing.read(file_path)
    # poj = file_name.split('__fdse__')[0] + '__fdse__' + file_name.split('__fdse__')[1].split('_')[0]
    poj = file_name.split("_2020")[0]

    Pojs_dependency_data[poj] = []
    for ele in dependency_content:
        if "version" not in ele.keys():
            continue
        groupId = ele["groupId"]
        artifactId = ele["artifactId"]
        version = ele["version"]
        path = ele["path"]

        # Pojs_GAV_path data
        GAV_str = groupId + '__fdse__' + artifactId + version
        if poj not in Pojs_GAV_Path.keys():
            Pojs_GAV_Path[poj] = {}
        if GAV_str not in Pojs_GAV_Path[poj].keys():
            Pojs_GAV_Path[poj][GAV_str] = [path]
        else:
            print("1111111111")
            Pojs_GAV_Path[poj][GAV_str].append(path)


        Pojs_dependency_data[poj].append( ele )

        GA = groupId + '__fdse__' + artifactId
        if GA in GA_dependency_data:
            if version in GA_dependency_data[GA].keys():
                # print(GA_dependency_data[GA])
                if poj not in GA_dependency_data[GA][version]:
                    GA_dependency_data[GA][version].append(poj)
            else:
                GA_dependency_data[GA][version] = [poj]
        else:
            GA_dependency_data[GA] = {version:[poj]}

def write():
    JSONFIle_processing.write(GA_dependency_data,"GAV_PojsDependency_data.json")
    JSONFIle_processing.write(Pojs_dependency_data,"Pojs_GAVDependency_data.json")
    JSONFIle_processing.write(Pojs_GAV_Path, "Pojs_GAV_Path.json")


def main():
    getFileList()
    for file_name in dependency_data_file_list:
        collectDependency(file_name)
    write()


main()






