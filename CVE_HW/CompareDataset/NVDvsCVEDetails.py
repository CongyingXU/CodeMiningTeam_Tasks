# -*- coding: utf-8 -*-

"""
Created on 2020-04-04 12:06  

@author: congyingxu
"""

from CommonFunction import JSONFIle_processing

CVE_CVEID_list_dir = '/Users/congyingxu/Downloads/CVE/MetaData/CVE_CVEID_list.json'
CVE_CVEID_list = JSONFIle_processing.read(CVE_CVEID_list_dir)


NVDDataset_dir = "/Users/congyingxu/Downloads/CVE/DataSet-NVD/"
NVDYearDataset = {}
NVD_CVEID_list_path = "/Users/congyingxu/Downloads/CVE/MetaData/NVD_CVEID_list.json"
NVD_CVEID_list = JSONFIle_processing.read(NVD_CVEID_list_path)
NVDItems_dir = "/Users/congyingxu/Downloads/CVE/DataSet-NVD/NVDItems/"


root_dir = "/Users/congyingxu/Downloads/"
CVEDetails_CVEID_list_path = root_dir + 'CVE/CrawledCVEdetailsHtmls/CVEDetails_CVEID_list.json'
CVEDetails_CVEID_list = JSONFIle_processing.read(CVEDetails_CVEID_list_path)
CVEDetails_pages_dir = "/Users/congyingxu/Downloads/CVE/CrawledCVEdetailsHtmls/Pages/"
CVEDetailsItems_dir = "/Users/congyingxu/Downloads/CVE/CrawledCVEdetailsHtmls/CVEDetailsItems/"


differet_data_path = "/Users/congyingxu/Downloads/CVE/NVDvsCVEdetails_Different.json"
differet_data = {}
differet_count  = 0



def compareItem(CVEID):
    global differet_count, differet_data, NVD_CVEID_list

    # if CVEID exists in NVD
    if CVEID not in NVD_CVEID_list or CVEID not in CVEDetails_CVEID_list:
        print('-------------------------CVEID not in NVD or not in CVEdetails')
        return

    extractCVEInfo()
    compareCVEInfo()



def extractCVEInfo():

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


    # extractInfo from CVEdetails
    CVE_CVEID_Info = CVEDictionary.extractCVEitemInfo(CVEID)
    CVE_CVEID_refs = CVE_CVEID_Info[CVEID]['refs']
    CVE_CVEID_desc = CVE_CVEID_Info[CVEID]['desc']
    CVE_CVEID_date = CVE_CVEID_Info[CVEID]['date']
    CVE_CVEID_refs = sorted(CVE_CVEID_refs)
    # print(CVE_CVEID_Info)


def compareCVEInfo():

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

    for CVEID in CVE_CVEID_list:
        print(CVEID)
        compareItem(CVEID)
        # break

    # JSONFIle_processing.write(json_content=differet_data , path=differet_data_path)
    # JSONFIle_processing.write(json_content=NVD_CVEID_list, path= NVD_CVEID_list_path)
    # print("differet_count: ", differet_count)

if __name__ == '__main__':
    main()