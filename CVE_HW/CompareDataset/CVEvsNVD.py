# -*- coding: utf-8 -*-

"""
Created on 2020-04-04 12:06  

@author: congyingxu

differet_count:  4715
"""

from CommonFunction import JSONFIle_processing
from CVE_HW.CompareDataset import ParseCVEDictionary
from CVE_HW import CONFIG
import urllib

CVEDictionary = ParseCVEDictionary.CVEDictionary()
CVEID_list = CVEDictionary.CVE_CVEID_list

# NVDDataset_dir = "/Users/congyingxu/Downloads/CVE/DataSet-NVD/"
NVDDataset_dir = CONFIG.NVDDataset_dir
NVDYearDataset = {}
# NVD_CVEID_list_path = "/Users/congyingxu/Downloads/CVE/MetaData/NVD_CVEID_list.json"
NVD_CVEID_list_path = CONFIG.NVD_CVEID_list_path
NVD_CVEID_list = JSONFIle_processing.read(NVD_CVEID_list_path)

# NVDItems_dir = "/Users/congyingxu/Downloads/CVE/DataSet-NVD/NVDItems/"
NVDItems_dir = CONFIG.NVDItems_dir

# differet_data_path = "/Users/congyingxu/Downloads/CVE/CVEvsNVD_Different.json"
differet_data_path = CONFIG.CVEvsNVD_Different_path
differet_data = {'ComparedCVEIDs':[],'NotInNVDCVEIDs':[],'vector':['0','desc','refs','ref_srcs']}
differet_count  = 0
JSONFIle_processing.write(json_content=differet_data , path=differet_data_path)

ComparedCVE_list = [] # 对比的列表
NotInNVDCVE_list = [] # 不存在yu

def readNVDYearData(year):
    global NVDYearDataset
    if year <= 2002:
        year =2002

    file_path = NVDDataset_dir + "nvdcve-1.1-" + str(year) +'.json'
    NVDYearDataset = JSONFIle_processing.read(file_path)

def compareItem(CVEID):
    global differet_count, differet_data, NVD_CVEID_list
    # if CVEID exists in NVD
    # if CVEID not in NVD_CVEID_list:
    #     # print('-------------------------CVEID not in NVD')
    #     differet_data['NotInNVDCVEIDs'].append(CVEID)
    #     return

    differet_data['ComparedCVEIDs'].append(CVEID)
    # extractInfo from NVD
    NVD_CVEID_info_path =NVDItems_dir + CVEID +'.json'
    try:
        NVD_CVEID_info = JSONFIle_processing.read(NVD_CVEID_info_path)
        NVD_CVEID_list.append(CVEID)
    except FileNotFoundError:
        if CVEID in NVD_CVEID_list:
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
        full_url = urllib.parse.unquote(urllib.parse.unquote(full_url))
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
        flag += 100
        print('dddddddddddddifferent: description')
        print("CVE_CVEID_desc", CVE_CVEID_desc)
        print("NVD_CVEID_desc", NVD_CVEID_desc)
        pass

    # reference
    CVE_CVEID_refs_list = sorted( [ele.split('__fdse__')[1] for ele in CVE_CVEID_refs] )
    NVD_CVEID_refs_list = sorted( [ele.split('__fdse__')[1] for ele in NVD_CVEID_refs] )

    CVE_CVEID_src_list = sorted( [ele.split('__fdse__')[0] for ele in CVE_CVEID_refs] )
    NVD_CVEID_src_list = sorted( [ele.split('__fdse__')[0] for ele in NVD_CVEID_refs] )

    if CVE_CVEID_refs == NVD_CVEID_refs:
        # print('sssssssssssssame: reference')
        # print("CVE_CVEID_refs", CVE_CVEID_refs)
        # print("NVD_CVEID_refs", NVD_CVEID_refs)

        pass
    else:

        print('dddddddddddddifferent: reference')
        print("CVE_CVEID_refs", CVE_CVEID_refs)
        print("NVD_CVEID_refs", NVD_CVEID_refs)
        pass

        if CVE_CVEID_refs_list != NVD_CVEID_refs_list:
            flag += 20
        if CVE_CVEID_src_list != NVD_CVEID_src_list:
            flag += 3

    if flag != 0:
        differet_count +=1
        differet_data[CVEID] = {}
        differet_data[CVEID]['flag'] = flag
        differet_data[CVEID]['CVE'] = {'desc': CVE_CVEID_desc, 'refs':CVE_CVEID_refs, 'src':CVE_CVEID_src_list}
        differet_data[CVEID]['NVD'] = {'desc': NVD_CVEID_desc, 'refs':NVD_CVEID_refs, 'src':NVD_CVEID_src_list}


def specialCondition():
    pass


def main():
    global differet_count, differet_data, NVD_CVEID_list, differet_data_path

    for CVEID in CVEID_list:
        print(CVEID)
        compareItem(CVEID)
        # break
    JSONFIle_processing.write(json_content=differet_data , path=differet_data_path)

    NVD_CVEID_list = list( set(NVD_CVEID_list) )
    JSONFIle_processing.write(json_content=NVD_CVEID_list, path= NVD_CVEID_list_path)
    print("differet_count: ", differet_count)




if __name__ == '__main__':
    main()
    # chuliyixia()


# CVE-2019-9865