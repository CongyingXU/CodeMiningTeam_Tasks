# -*- coding: utf-8 -*-

"""
Created on 2020-02-17 21:31  

@author: congyingxu
"""
from CommonFunction import File_processing
import json

CVE_Dataset_path = "/Users/congyingxu/Documents/FDSE_lab/CodeMiningTeam/CongyingXU/CVE/Dataset/"
CVE_VPV_Data_path = "Local_Data/CVE_VulnerableVP.json"

file_list = []
CVE_VPV_Data = {}


fields = set()
def getFileList():
    global file_list
    file_list = File_processing.walk_L1_FileNames(CVE_Dataset_path)

def readFile(path):
    with open(path,"r") as f:
        file_data = json.loads( f.read() )

    return file_data

def collectVulberableCPE(cpe_match):
    global fields

    VulberableCPE_set = set()
    # print(VulberableCPE_set)
    for match_ele in cpe_match:
        fields.update(  set( match_ele.keys() ) )
        vulnerable = match_ele["vulnerable"]
        if not vulnerable:
            continue
            # cpe23Uri = match_ele["cpe23Uri"]
            # cpe_ID = cpe23Uri.split(":")[3] + "__fdse__" + cpe23Uri.split(":")[4]
            # VulberableCPE_set.add(cpe_ID)
            # print("false:",match_ele)
        else:
            # 版本号暂时不拿
            cpe23Uri = match_ele["cpe23Uri"]

            Version_Num = cpe23Uri.split(":")[5]
            if Version_Num == '*' or Version_Num == '-':
                Version_Num = "NA"

            Version_InFo = "Version_Num:" + Version_Num

            Version_Num = "NA"
            #   是否会有其他子弹的可能？
            if "versionStartIncluding" in match_ele.keys():
                Version_Num = match_ele["versionStartIncluding"]
            Version_InFo += "||versionStartIncluding:" + Version_Num
            Version_Num = "NA"
            #   是否会有其他子弹的可能？
            if "versionEndIncluding" in match_ele.keys():
                Version_Num = match_ele["versionEndIncluding"]
            Version_InFo += "||versionEndIncluding:" + Version_Num
            Version_Num = "NA"
            #   是否会有其他子弹的可能？
            if "versionStartExcluding" in match_ele.keys():
                Version_Num = match_ele["versionStartExcluding"]
            Version_InFo += "||versionStartExcluding:" + Version_Num
            Version_Num = "NA"
            #   是否会有其他子弹的可能？
            if "versionEndExcluding" in match_ele.keys():
                Version_Num = match_ele["versionEndExcluding"]
            Version_InFo += "||versionEndExcluding:" + Version_Num




            cpe_ID = cpe23Uri.split(":")[3] + "__fdse__" + cpe23Uri.split(":")[4] + "__fdse__" + Version_InFo
            VulberableCPE_set.add(cpe_ID)
            # print(match_ele)
        # break

    return VulberableCPE_set


def collectCVEtoVPV(file_data):
    global cveItem_VulberableCPE_set

    for cve_item in file_data["CVE_Items"]:
        cve_ID = cve_item["cve"]["CVE_data_meta"]["ID"]
        nodes = cve_item["configurations"]["nodes"]

        cveItem_VulberableCPE_set =set()
        # print(cveItem_VulberableCPE_set)

        for node in nodes:
            # 13年类似版
            special_key = "children"
            if special_key in node.keys():
                children = node[special_key]
                for children_ele in children:
                    cpe_match = children_ele["cpe_match"]
                    VulberableCPE_set = collectVulberableCPE(cpe_match)
                    cveItem_VulberableCPE_set.update( VulberableCPE_set )
            else:
                # 19年类似版本
                print(node)
                if "cpe_match" in node.keys():
                    cpe_match = node["cpe_match"]
                    VulberableCPE_set = collectVulberableCPE(cpe_match)
                    cveItem_VulberableCPE_set.update(VulberableCPE_set)


        CVE_VPV_Data[cve_ID] = list( cveItem_VulberableCPE_set )



def write():
    with open(CVE_VPV_Data_path,'w') as f:
        f.write( json.dumps( CVE_VPV_Data,indent=4 ) )

def main():
    getFileList()
    for data_file in file_list:
        if data_file.endswith(".DS_Store"):
            continue

        print(data_file)
        data_file_path = CVE_Dataset_path + data_file
        file_data = readFile( data_file_path )
        collectCVEtoVPV(file_data)
        # break

    write()

main()
print("CVE length:", len(CVE_VPV_Data.keys()))
print("fields: ",fields)