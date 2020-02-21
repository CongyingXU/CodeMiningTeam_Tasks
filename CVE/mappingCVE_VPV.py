# -*- coding: utf-8 -*-

"""
Created on 2020-02-17 21:31  

@author: congyingxu
"""
from CommonFunction import File_processing, JSONFIle_processing
import json

CVE_Dataset_path = "/Users/congyingxu/Documents/FDSE_lab/CodeMiningTeam/CongyingXU/CVE/Dataset/"
CVE_VPV_Data_path = "Local_Data/CVE_VulnerableVP.json"
VPV_CVE_Data_path = "Local_Data/VulnerableVP_CVE.json"


file_list = []
CVE_VPV_Data = {}
VPV_CVE_Data = {}


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
            if "versionStartIncluding" in match_ele.keys():
                Version_Num = match_ele["versionStartIncluding"]
            Version_InFo += "||versionStartIncluding:" + Version_Num
            Version_Num = "NA"
            if "versionEndIncluding" in match_ele.keys():
                Version_Num = match_ele["versionEndIncluding"]
            Version_InFo += "||versionEndIncluding:" + Version_Num
            Version_Num = "NA"
            if "versionStartExcluding" in match_ele.keys():
                Version_Num = match_ele["versionStartExcluding"]
            Version_InFo += "||versionStartExcluding:" + Version_Num
            Version_Num = "NA"
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
                # print(node)
                if "cpe_match" in node.keys():
                    cpe_match = node["cpe_match"]
                    VulberableCPE_set = collectVulberableCPE(cpe_match)
                    cveItem_VulberableCPE_set.update(VulberableCPE_set)


        CVE_VPV_Data[cve_ID] = list( cveItem_VulberableCPE_set )



def getVersion(version_str):

    # Version_Num:NA||versionStartIncluding:NA||versionEndIncluding:NA||versionStartExcluding:NA||versionEndExcluding:NA
    version_info_list = version_str.split('||')
    Version_Num = version_info_list[0].split(':')[1]
    versionStartIncluding = version_info_list[1].split(':')[1]
    versionEndIncluding = version_info_list[2].split(':')[1]
    versionStartExcluding = version_info_list[3].split(':')[1]
    versionEndExcluding = version_info_list[4].split(':')[1]

    versin_item = {}

    for ele in version_info_list:
        ele_name = ele.split(':')[0]
        ele_value = ele.split(':')[1]
        if ele_value != 'NA':
            versin_item[ele_name] = ele_value


    # return { "Version_Num":Version_Num, "versionStartIncluding": versionStartIncluding,"versionEndIncluding":versionEndIncluding,"versionStartExcluding":versionStartExcluding, "versionEndExcluding":versionEndExcluding  }
    return versin_item



def getVersionStr(version_str):

    # Version_Num:NA||versionStartIncluding:NA||versionEndIncluding:NA||versionStartExcluding:NA||versionEndExcluding:NA
    version_info_list = version_str.split('||')

    versin_str_item = ''

    for ele in version_info_list:
        ele_name = ele.split(':')[0]
        ele_value = ele.split(':')[1]
        if ele_value != 'NA':
            versin_str_item += "||" + ele


    return versin_str_item.strip("")


# 单独整理version信息
def reorganizeData():
    global CVE_VPV_Data,VPV_CVE_Data

    temp = {}
    for CVE_ID in CVE_VPV_Data.keys():

        VPV_item = {}
        for ele in CVE_VPV_Data[CVE_ID]:
            # print(CVE_VPV_Data[CVE_ID])
            VP = ele.split("__fdse__")[0] + "__fdse__" + ele.split("__fdse__")[1]
            version_str = ele.split("__fdse__")[2]

            # Data one
            if CVE_ID in temp.keys():
                if VP in temp[CVE_ID].keys():
                    if getVersion(version_str) in temp[CVE_ID][VP]:
                        print(ele)
                    else:
                        temp[CVE_ID][VP].append( getVersion(version_str) )
                else:
                    temp[CVE_ID][VP] = [ getVersion(version_str) ]
            else:
                temp[CVE_ID] = { VP : [ getVersion(version_str) ] }


            # Data  two
            if VP in VPV_CVE_Data.keys():
                if version_str in VPV_CVE_Data[VP].keys():
                    VPV_CVE_Data[VP][version_str].append( CVE_ID )
                else:
                    VPV_CVE_Data[VP][version_str] = [CVE_ID]
            else:
                VPV_CVE_Data[VP] = {  version_str : [CVE_ID] }


    CVE_VPV_Data = temp





def write():
    with open(CVE_VPV_Data_path,'w') as f:
        f.write( json.dumps( CVE_VPV_Data,indent=4 ) )

    with open(VPV_CVE_Data_path,'w') as f:
        f.write( json.dumps( VPV_CVE_Data,indent=4 ) )

def main():
    getFileList()
    for data_file in file_list:
        if data_file.endswith(".DS_Store"):
            continue

        # print(data_file)
        data_file_path = CVE_Dataset_path + data_file
        file_data = readFile( data_file_path )
        collectCVEtoVPV(file_data)

        # break
    reorganizeData()
    write()

main()
print("CVE length:", len(CVE_VPV_Data.keys()))
print("fields: ",fields)