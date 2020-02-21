# -*- coding: utf-8 -*-

"""
Created on 2020-02-18 16:05  

@author: congyingxu
"""
import sys
sys.path.append('../')  # 新加入的

from CommonFunction import File_processing
from bs4 import BeautifulSoup
import json


CVE_LocalVPRepo_path = "/home/hadoop/dfs/data/Workspace/CVE_VP_Repositories/"

LocalRepo_VP_list = []
LocalRepoVP_POMGA_Data = {}

def getVP_list():
    global LocalRepo_VP_list
    folder_list = File_processing.walk_L1_Folders(CVE_LocalVPRepo_path)
    LocalRepo_VP_list  = folder_list
    print("len foldr_list: ",len(folder_list))



def findPOM(path):
    # /home/hadoop/dfs/data/Workspace/CVE_VP_Repositories/V__fdse__P/
    print("path: ",path)
    # 控制层数,5
    if len( path.split('/') ) > 5 + 5 :
        return



    file_list = File_processing.walk_L1_FileNames(path)
    for file_name in file_list:
        if file_name.find('.') > -1:  # 文件
            if file_name.lower() == "pom.xml":
                file_full_path  = path + file_name
                parseGAInfo(file_full_path)

            else:
                pass

    # 文件夹
    folder_list = File_processing.walk_L1_Folders(path)
    for folder_name in folder_list:
        folder_full_path = path + folder_name + '/'
        findPOM(folder_full_path)



def parseGAInfo(pom_full_path):
    # print(pom_full_path)
    with open(pom_full_path,'r') as f:
        xml = f.read()

    soup = BeautifulSoup(xml, 'html.parser')
    project = soup.find('project')

    groupId = ''
    artifactId = ''
    version = ''

    parent = project.find("parent")

    if parent != None:
        # print(parent)
        for ele in parent:
            if ele.name == "groupid":
                groupId = ele.get_text()
            elif ele.name == "artifactid":
                artifactId = ele.get_text()
            elif ele.name == "version":
                version = ele.get_text()

    for ele in project:
        if ele.name == "groupid":
            groupId = ele.get_text()
        elif ele.name == "artifactid":
            artifactId = ele.get_text()
        elif ele.name == "version":
            version = ele.get_text()

    VP_name = ''
    for folder_name in pom_full_path.split("/"):
        if "__fdse__" in folder_name :
            VP_name = folder_name
            break

    item = { "groupId":groupId , "artifactId":artifactId , "POM_path": pom_full_path }
    if VP_name in LocalRepoVP_POMGA_Data.keys():
        LocalRepoVP_POMGA_Data[VP_name].append( item )
    else:
        LocalRepoVP_POMGA_Data[VP_name] = [item]

    # print(LocalRepoVP_POMGA_Data)


def write():
    with open("LocalRepoVP_POMGA_iteration.json",'w') as f:
        f.write( json.dumps(LocalRepoVP_POMGA_Data) )

# parseGAInfo("pom.xml")


def main():
    global LocalRepoVP_POMGA_Data
    getVP_list()
    with open("LocalRepoVP_POMGA_iteration.json",'r') as f:
        LocalRepoVP_POMGA_Data = json.loads( f.read() )

    for VP in LocalRepo_VP_list:

        if VP in LocalRepoVP_POMGA_Data.keys():
            print("Pass VP: ", VP)
            continue
        print("VP: ", VP)
        VP_Repo_path = CVE_LocalVPRepo_path + VP + '/'
        findPOM(VP_Repo_path)

        print("write!")
        write()



def readresult():
    global LocalRepoVP_POMGA_Data
    with open("/Users/congyingxu/Downloads/LocalRepoVP_POMGA_iteration.json",'r') as f:
        LocalRepoVP_POMGA_Data = json.loads( f.read() )
    print("len:", len( LocalRepoVP_POMGA_Data.keys() ))

    with open("Local_Data/CPE_VP_LocalRepo.json",'r') as f:
        content = json.loads( f.read() )

    # for VP in content.keys():
    #     if VP not in LocalRepoVP_POMGA_Data.keys():
    #         print(VP)

def collect_result():
    CVE_GAInfo = {}
    GA_list = set()
    for VP in LocalRepoVP_POMGA_Data.keys():
        for ele in LocalRepoVP_POMGA_Data[VP]:
            G = ele["groupId"]
            A = ele["artifactId"]
            pom_path = ele["POM_path"]

            GA = G +'__fdse__' + A
            if GA in CVE_GAInfo.keys():
                if len(pom_path) < len( CVE_GAInfo[GA]["POM_path"] ):
                    CVE_GAInfo[GA] = {"VendorProduct": VP, "POM_path": pom_path}
                    # print("Duplicate GA: ", GA)
                    # print(pom_path)
                    pass
                else:
                    continue
            else:
                CVE_GAInfo[GA] = {"VendorProduct": VP, "POM_path": pom_path}

    write_collect_result(CVE_GAInfo)

def write_collect_result(CVE_GAInfo):
    with open("Local_Data/CVE_GAInfo.json",'w') as f:
        f.write( json.dumps(CVE_GAInfo, indent=4) )
    print("len CVE GA:", len(  CVE_GAInfo.keys() ))


def collectresult_main():
    readresult()
    collect_result()

    pass


collectresult_main()


# main()