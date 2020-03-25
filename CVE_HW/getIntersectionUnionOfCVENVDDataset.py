# -*- coding: utf-8 -*-

"""
Created on 2020-03-11 12:52  

@author: congyingxu

len CVE_CVEID_list 170801
len NVD_CVEID_list 139870
len unionID_list 170801
len intersectionID_list 139870
len CVE_complementID_list 30931
len NVD_complementID_list 0

"""

from CommonFunction import JSONFIle_processing, File_processing
from bs4 import BeautifulSoup



CVE_dataset_file_path = "/Users/congyingxu/Downloads/CVE/allitems.xml"
NVD_dataset_folder_path = "/Users/congyingxu/Downloads/NVD/"

CVE_dataset = '' # xml
NVD_dataset = {}

CVE_CVEID_list = []
NVD_CVEID_list = []

unionID_list = []
intersectionID_list = []
CVE_complementID_list = []
NVD_complementID_list = []


def extractXML(CVE_dataset):
    print("Start to extractXML")

    ID_list = []

    xml = CVE_dataset
    # soup = BeautifulSoup(xml, 'html.parser')
    soup = BeautifulSoup(xml, 'lxml')
    # item_list = soup.find_all('item', attrs={'type': 'CVE'})
    item_list = soup.find_all('item')
    for cve_item in item_list:
        cve_ID = cve_item["name"]
        ID_list.append(cve_ID)
        # print(cve_ID)
        # break

    return ID_list

def read():
    print("Start to read")
    global CVE_dataset,NVD_dataset
    CVE_dataset = File_processing.read_TXTfile(CVE_dataset_file_path)
    NVD_dataset_file_list = File_processing.walk_L1_FileNames(NVD_dataset_folder_path)
    # print(NVD_dataset_file_list)
    for file in NVD_dataset_file_list:
        if '.json' in file:
            file_content = JSONFIle_processing.read(NVD_dataset_folder_path + file)
            NVD_dataset[file] =  file_content

def collectData():
    print("Start to collectData")
    global CVE_CVEID_list, NVD_CVEID_list

    # # get NVD_CVEID_list
    # print(NVD_dataset.keys())
    for year_data in NVD_dataset.keys():
        CVE_Items  = NVD_dataset[year_data]["CVE_Items"]
        for cve_item in CVE_Items:
            cve_ID = cve_item["cve"]["CVE_data_meta"]["ID"]
            NVD_CVEID_list.append(cve_ID)
            # print(cve_ID)
            # break
    # get CVE_CVEID_list, NVD_CVEID_list
    CVE_CVEID_list = extractXML(CVE_dataset)


    global unionID_list, intersectionID_list, CVE_complementID_list, NVD_complementID_list

    unionID_list = set()
    CVE_CVEID_list = set(CVE_CVEID_list)
    NVD_CVEID_list = set(NVD_CVEID_list)

    unionID_list = CVE_CVEID_list.union(NVD_CVEID_list)
    intersectionID_list = CVE_CVEID_list.intersection(NVD_CVEID_list)
    intersectionID_list_temp = NVD_CVEID_list.intersection(CVE_CVEID_list)

    CVE_complementID_list = CVE_CVEID_list.difference(NVD_CVEID_list)
    NVD_complementID_list = NVD_CVEID_list.difference(CVE_CVEID_list)

    # for cve_ID in NVD_CVEID_list:
    #     if cve_ID in CVE_CVEID_list:
    #         intersectionID_list.append(cve_ID)
    #     else:
    #         NVD_complementID_list.append(cve_ID)
    #     unionID_list.add(cve_ID)
    #
    # # check intersectionID_list_temp
    # intersectionID_list_temp = []
    # for cve_ID in CVE_CVEID_list:
    #     if cve_ID in NVD_CVEID_list:
    #         intersectionID_list_temp.append(cve_ID)
    #     else:
    #         CVE_complementID_list.append(cve_ID)
    #     unionID_list.add(cve_ID)
    # unionID_list = list( unionID_list )
    # intersectionID_list_temp = list( set(intersectionID_list_temp) )
    # intersectionID_list = list(set(intersectionID_list))

    print("len intersectionID_list_temp",len(intersectionID_list_temp))
    print("len intersectionID_list", len(intersectionID_list))



def write():
    global CVE_CVEID_list, NVD_CVEID_list

    CVE_CVEID_list = list(CVE_CVEID_list)
    NVD_CVEID_list = list(NVD_CVEID_list)
    JSONFIle_processing.write(CVE_CVEID_list, 'Data/CVE_CVEID_list.json')
    JSONFIle_processing.write(NVD_CVEID_list, 'Data/NVD_CVEID_list.json')
    print("len CVE_CVEID_list",len(CVE_CVEID_list))
    print("len NVD_CVEID_list", len(NVD_CVEID_list))

    global unionID_list, intersectionID_list, CVE_complementID_list, NVD_complementID_list
    unionID_list = list(unionID_list)
    intersectionID_list = list(intersectionID_list)
    CVE_complementID_list = list(CVE_complementID_list)
    NVD_complementID_list = list(NVD_complementID_list)
    JSONFIle_processing.write(unionID_list, 'Data/unionID_list.json')
    JSONFIle_processing.write(intersectionID_list, 'Data/intersectionID_list.json')
    JSONFIle_processing.write(CVE_complementID_list, 'Data/CVE_complementID_list.json')
    JSONFIle_processing.write(NVD_complementID_list, 'Data/NVD_complementID_list.json')
    print("len unionID_list", len(unionID_list))
    print("len intersectionID_list", len(intersectionID_list))
    print("len CVE_complementID_list", len(CVE_complementID_list))
    print("len NVD_complementID_list", len(NVD_complementID_list))


if __name__ == '__main__':
    read()
    collectData()
    write()