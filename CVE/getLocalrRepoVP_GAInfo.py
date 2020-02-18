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
    print("path: ",path)

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
    with open("LocalRepoVP_POMGA.json",'w') as f:
        f.write( json.dumps(LocalRepoVP_POMGA_Data) )

# parseGAInfo("pom.xml")


def main():
    getVP_list()

    for VP in LocalRepo_VP_list:
        print("VP: ",VP)
        VP_Repo_path = CVE_LocalVPRepo_path + VP + '/'
        findPOM(VP_Repo_path)

    print("write!")
    write()

main()