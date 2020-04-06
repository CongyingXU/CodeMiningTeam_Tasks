# -*- coding: utf-8 -*-

"""
Created on 2020-04-04 12:06  

@author: congyingxu

differet_count:  4715
"""

from CommonFunction import JSONFIle_processing
from CVE_HW.CompareDataset import ParseCVEDictionary

CVEDictionary = ParseCVEDictionary.CVEDictionary()
CVEID_list = CVEDictionary.CVE_CVEID_list

NVDDataset_dir = "/Users/congyingxu/Downloads/CVE/DataSet-NVD/"
NVDYearDataset = {}
NVD_CVEID_list_path = "/Users/congyingxu/Downloads/CVE/MetaData/NVD_CVEID_list.json"
NVD_CVEID_list = JSONFIle_processing.read(NVD_CVEID_list_path)

NVDItems_dir = "/Users/congyingxu/Downloads/CVE/DataSet-NVD/NVDItems/"

differet_data_path = "/Users/congyingxu/Downloads/CVE/CVEvsNVD_Different.json"
differet_data = {}
differet_count  = 0

def readNVDYearData(year):
    global NVDYearDataset
    if year <= 2002:
        year =2002

    file_path = NVDDataset_dir + "nvdcve-1.1-" + str(year) +'.json'
    NVDYearDataset = JSONFIle_processing.read(file_path)

def compareItem(CVEID):
    global differet_count, differet_data, NVD_CVEID_list
    # if CVEID exists in NVD
    if CVEID not in NVD_CVEID_list:
        # print('-------------------------CVEID not in NVD')
        return

    # extractInfo from NVD
    NVD_CVEID_info_path =NVDItems_dir + CVEID +'.json'
    try:
        NVD_CVEID_info = JSONFIle_processing.read(NVD_CVEID_info_path)
    except FileNotFoundError:
        NVD_CVEID_list.remove(CVEID)
        # print(CVEID)
        return
    NVD_CVEID_desc = NVD_CVEID_info['cve']['description']['description_data'][0]['value']
    NVD_CVEID_date = NVD_CVEID_info['publishedDate']
    NVD_CVEID_refs = []
    for ele in NVD_CVEID_info['cve']['references']['reference_data']:
        url = ele['url']
        src = ele['refsource']
        full_url = src + "__fdse__" + url
        NVD_CVEID_refs.append(full_url.replace('&amp;','&'))
    NVD_CVEID_refs = sorted(NVD_CVEID_refs)
    # print(NVD_CVEID_info)

    # extractInfo from CVE
    CVE_CVEID_Info = CVEDictionary.extractCVEitemInfo(CVEID)
    CVE_CVEID_refs = CVE_CVEID_Info[CVEID]['refs']
    CVE_CVEID_desc = CVE_CVEID_Info[CVEID]['desc']
    CVE_CVEID_date = CVE_CVEID_Info[CVEID]['date']
    CVE_CVEID_refs = sorted(CVE_CVEID_refs)
    # print(CVE_CVEID_Info)

    # compare
    flag = 0
    # desc
    if CVE_CVEID_desc == NVD_CVEID_desc:
        # print('sssssssssssssame: description')
        # print("CVE_CVEID_desc", CVE_CVEID_desc)
        # print("NVD_CVEID_desc", NVD_CVEID_desc)

        pass
    else:
        flag = 10
        print('dddddddddddddifferent: description')
        print("CVE_CVEID_desc", CVE_CVEID_desc)
        print("NVD_CVEID_desc", NVD_CVEID_desc)
        pass

    # reference
    if CVE_CVEID_refs == NVD_CVEID_refs:
        # print('sssssssssssssame: reference')
        # print("CVE_CVEID_refs", CVE_CVEID_refs)
        # print("NVD_CVEID_refs", NVD_CVEID_refs)

        pass
    else:
        flag += 2
        print('dddddddddddddifferent: reference')
        print("CVE_CVEID_refs", CVE_CVEID_refs)
        print("NVD_CVEID_refs", NVD_CVEID_refs)
        pass

    if flag != 0:
        differet_count +=1
        differet_data[CVEID] = {}
        differet_data[CVEID]['flag'] = flag
        differet_data[CVEID]['CVE'] = {'desc': CVE_CVEID_desc, 'refs':CVE_CVEID_refs}
        differet_data[CVEID]['NVD'] = {'desc': NVD_CVEID_desc, 'refs':NVD_CVEID_refs}


def specialCondition():
    pass


def main():
    global differet_count, differet_data, NVD_CVEID_list

    for CVEID in CVEID_list:
        print(CVEID)
        compareItem(CVEID)
        # break
    JSONFIle_processing.write(json_content=differet_data , path=differet_data_path)
    JSONFIle_processing.write(json_content=NVD_CVEID_list, path= NVD_CVEID_list_path)
    print("differet_count: ", differet_count)

if __name__ == '__main__':
    main()
