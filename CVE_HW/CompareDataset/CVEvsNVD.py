# -*- coding: utf-8 -*-

"""
Created on 2020-04-04 12:06  

@author: congyingxu

CVE-2019-12428
CVE-2019-12429
CVE-2019-12430
CVE-2019-12431
CVE-2019-12432
CVE-2019-12433
CVE-2019-12434
CVE-2019-12441
CVE-2019-12442
CVE-2019-12443
CVE-2019-12444
CVE-2019-12445
CVE-2019-12446
CVE-2019-13001
CVE-2019-13002
CVE-2019-13003
CVE-2019-13004
CVE-2019-13005
CVE-2019-13006
CVE-2019-13007
CVE-2019-13009
CVE-2019-13010
CVE-2019-13011
CVE-2019-13121
CVE-2019-13457
CVE-2019-15034
CVE-2019-17636
CVE-2019-18336
CVE-2019-19277
CVE-2019-19279
CVE-2019-19281
CVE-2019-19282
CVE-2019-19290
CVE-2019-19291
CVE-2019-19292
CVE-2019-19293
CVE-2019-19294
CVE-2019-19295
CVE-2019-19296
CVE-2019-19297
CVE-2019-19298
CVE-2019-19299
CVE-2019-20509
CVE-2019-3553
CVE-2019-4608
CVE-2019-6585
CVE-2019-7589
CVE-2019-9859
CVE-2020-0010
CVE-2020-0011
CVE-2020-0012
CVE-2020-0029
CVE-2020-0031
CVE-2020-0032
CVE-2020-0033
CVE-2020-0034
CVE-2020-0035
CVE-2020-0036
CVE-2020-0037
CVE-2020-0038
CVE-2020-0039
CVE-2020-0041
CVE-2020-0042
CVE-2020-0043
CVE-2020-0044
CVE-2020-0045
CVE-2020-0046
CVE-2020-0047
CVE-2020-0048
CVE-2020-0049
CVE-2020-0050
CVE-2020-0051
CVE-2020-0052
CVE-2020-0053
CVE-2020-0054
CVE-2020-0055
CVE-2020-0056
CVE-2020-0057
CVE-2020-0058
CVE-2020-0059
CVE-2020-0060
CVE-2020-0061
CVE-2020-0062
CVE-2020-0063
CVE-2020-0066
CVE-2020-0069
CVE-2020-0083
CVE-2020-0084
CVE-2020-0085
CVE-2020-0087
CVE-2020-10255
CVE-2020-10372
CVE-2020-4162
CVE-2020-5253
CVE-2020-5254
CVE-2020-5258
CVE-2020-5259
CVE-2020-6178
CVE-2020-6196
CVE-2020-6197
CVE-2020-6198
CVE-2020-6199
CVE-2020-6200
CVE-2020-6201
CVE-2020-6202
CVE-2020-6203
CVE-2020-6204
CVE-2020-6205
CVE-2020-6206
CVE-2020-6207
CVE-2020-6208
CVE-2020-6209
CVE-2020-6210
CVE-2020-7579
CVE-2020-9044
CVE-2020-9440
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
