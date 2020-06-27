# -*- coding: utf-8 -*-

"""
Created on 2020-04-04 12:06  

@author: congyingxu
"""

from CommonFunction import JSONFIle_processing
from CVE_HW_DatasetComparison.CrawlCVEDetails import ParseCVEDetails
from CVE_HW_DatasetComparison.CrawlerNVD import ParseNVD
from CVE_HW_DatasetComparison import CONFIG


CVE_CVEID_list_dir =  CONFIG.CVE_CVEID_list_dir
CVE_CVEID_list = sorted( JSONFIle_processing.read(CVE_CVEID_list_dir) )


NVDDataset_dir =  CONFIG.NVDDataset_dir
NVDYearDataset = {}
NVD_CVEID_list_path = CONFIG.NVD_CVEID_list_path
NVD_CVEID_list = JSONFIle_processing.read(NVD_CVEID_list_path)
NVDItems_dir = CONFIG.NVDItems_dir


CVEDetails_CVEID_list_path = CONFIG.CVEDetails_CVEID_list_path
CVEDetails_CVEID_list = JSONFIle_processing.read(CVEDetails_CVEID_list_path)
CVEDetails_pages_dir = CONFIG.CVEDetails_pages_dir
CVEDetailsItems_dir = CONFIG.CVEdetialsItems_dir


differet_data_path = CONFIG.NVDvsCVEdetails_Different_path
differet_data = {'ComparedCVEIDs':[],'NotInNVDCVEIDs':[],'NotInCVEdetailsCVEIDs':[], 'vector':['0','desc','refs','CVSS', 'CWE','AffectedVP', 'AffectedVPV', 'OvalDefinition']}
differet_count  = 0

ComparedCVEIDs = [] # 对比的列表
NotInNVDCVEIDs = [] # 不存在yu
NotInCVEdetailsCVEIDs = [] # 不存在yu

def compareItem(CVEID):
    global differet_count, differet_data, NVD_CVEID_list, ComparedCVEIDs, NotInNVDCVEIDs, NotInCVEdetailsCVEIDs

    # if CVEID exists in NVD
    if CVEID not in NVD_CVEID_list:
        print('-------------------------CVEID not in NVD')
        # NotInNVDCVEIDs.append(CVEID)
        differet_data['NotInNVDCVEIDs'].append(CVEID)
        # return
    if CVEID not in CVEDetails_CVEID_list:
        print('-------------------------CVEID not in CVEdetails')
        # NotInCVEdetailsCVEIDs.append(CVEID)
        differet_data['NotInCVEdetailsCVEIDs'].append(CVEID)
        # return
    if CVEID not in NVD_CVEID_list or CVEID not in CVEDetails_CVEID_list:
        return

    CVEdetialsItem = ParseCVEDetails.extractCVEdetailsItemInfo(CVEID)
    NVDItem = ParseNVD.extractNVDItemInfo(CVEID)
    compareCVEInfo(CVEdetialsItem, NVDItem, CVEID)
    differet_data['ComparedCVEIDs'].append(CVEID)


def compareCVEInfo(CVEdetialsItem, NVDItem, CVEID):
    global differet_count,differet_data

    # compare: description、reference、CVSS、CWE, **Affected Vendor Product** , **Affected VPV**, OvalDefinition
    field_num = 7
    flag = 0
    # description
    if CVEdetialsItem.Description ==NVDItem.Description:
        # print('sssssssssssssame: description')
        # print("CVEdetials_CVEID_desc", CVEdetialsItem.Description)
        # print("NVD_CVEID_desc", NVDItem.Description)

        pass
    else:
        flag = 1 * pow(10, field_num -1 )
        # print('dddddddddddddifferent: description')
        # print("CVEdetials_CVEID_desc", CVEdetialsItem.Description)
        # print("NVD_CVEID_desc", NVDItem.Description)
        pass

    # reference
    if CVEdetialsItem.Reference == NVDItem.Reference:
        # print('sssssssssssssame: reference')
        # print("CVEdetials_CVEID_Reference", CVEdetialsItem.Reference)
        # print("NVD_CVEID_Reference", NVDItem.Reference)

        pass
    else:
        flag += 2 * pow(10, field_num -2 )
        # print('dddddddddddddifferent: Reference')
        # print("CVEdetials_CVEID_Reference", CVEdetialsItem.Reference)
        # print("NVD_CVEID_Reference",  NVDItem.Reference)
        pass

    # CVSS
    if CVEdetialsItem.CVSS2 == NVDItem.CVSS2:
        # print('sssssssssssssame: reference')
        # print("CVEdetials_CVEID_CVSS2", CVEdetialsItem.CVSS2)
        # print("NVD_CVEID_CVSS2", NVDItem.CVSS2)

        pass
    else:
        flag += 3 * pow(10, field_num - 3)
        # print('dddddddddddddifferent: CVSS2')
        # print("CVEdetials_CVEID_CVSS2", CVEdetialsItem.CVSS2)
        # print("NVD_CVEID_CVSS2", NVDItem.CVSS2)
        pass

    # CWE
    if CVEdetialsItem.CWE == NVDItem.CWE:
        # print('sssssssssssssame: reference')
        # print("CVEdetials_CVEID_CWE", CVEdetialsItem.CWE)
        # print("NVD_CVEID_CWE", NVDItem.CWE)

        pass
    else:
        flag += 4 * pow(10, field_num - 4)
        # print('dddddddddddddifferent: CWE')
        # print("CVEdetials_CVEID_CWE", CVEdetialsItem.CWE)
        # print("NVD_CVEID_CWE", NVDItem.CWE)
        pass

    # Affected Vendor Product
    if CVEdetialsItem.AffectedVendorProductCPE == NVDItem.AffectedVendorProductCPE:
        # # print('sssssssssssssame: reference')
        # print("CVEdetials_CVEID_AffectedVendorProductCPE", CVEdetialsItem.AffectedVendorProductCPE)
        # print("NVD_CVEID_AffectedVendorProductCPE", NVDItem.AffectedVendorProductCPE)

        pass
    else:
        flag += 5 * pow(10, field_num - 5)
        # print('dddddddddddddifferent: AffectedVendorProductCPE')
        # print("CVEdetials_CVEID_AffectedVendorProductCPE", CVEdetialsItem.AffectedVendorProductCPE)
        # print("NVD_CVEID_AffectedVendorProductCPE", NVDItem.AffectedVendorProductCPE)
        pass

    # Affected Vendor Product Version
    if CVEdetialsItem.AffectedVendorProductVersionCPE == NVDItem.AffectedVendorProductVersionCPE:
        # # print('sssssssssssssame: AffectedVendorProductVersionCPE')
        # print("CVEdetials_CVEID_AffectedVendorProductVersionCPE", CVEdetialsItem.AffectedVendorProductVersionCPE)
        # print("NVD_CVEID_AffectedVendorProductVersionCPE", NVDItem.AffectedVendorProductVersionCPE)

        pass
    else:
        flag += 6 * pow(10, field_num - 6)
        # print('dddddddddddddifferent: AffectedVendorProductVersionCPE')
        # print("CVEdetials_CVEID_AffectedVendorProductVersionCPE", CVEdetialsItem.AffectedVendorProductVersionCPE)
        # print("NVD_CVEID_AffectedVendorProductVersionCPE", NVDItem.AffectedVendorProductVersionCPE)
        pass

    # OvalDefinition
    if CVEdetialsItem.OvalDefinition == NVDItem.OvalDefinition:
        # # print('sssssssssssssame: OvalDefinition')
        # print("CVEdetials_CVEID_AffectedVendorProductVersionCPE", CVEdetialsItem.OvalDefinition)
        # print("NVD_CVEID_AffectedVendorProductVersionCPE", NVDItem.OvalDefinition)

        pass
    else:
        flag += 7 * pow(10, field_num - 7)
        # print('dddddddddddddifferent: OvalDefinition')
        # print("CVEdetials_CVEID_AOvalDefinition", CVEdetialsItem.OvalDefinition)
        # print("NVD_CVEID_OvalDefinition", NVDItem.OvalDefinition)
        pass

    if flag != 0:
        print(flag)
        differet_count +=1
        differet_data[CVEID] = {}
        differet_data[CVEID]['flag'] = flag
        differet_data[CVEID]['CVEdetails'] = CVEdetialsItem.toDict()
        differet_data[CVEID]['NVD'] = NVDItem.toDict()






def main():
    global differet_count, differet_data, NVD_CVEID_list

    for CVEID in CVE_CVEID_list:
        print(CVEID)
        # CVEID = 'CVE-2005-0834'
        # CVEID = 'CVE-1999-0088'
        compareItem(CVEID)
        # break
    # differet_data
    JSONFIle_processing.write(json_content=differet_data , path=differet_data_path)
    print("differet_count: ", differet_count)


def chuliyixia():
    NVD_CVEID_list = JSONFIle_processing.read(NVD_CVEID_list_path)
    NVD_CVEID_list = list(set(NVD_CVEID_list))
    JSONFIle_processing.write(json_content=NVD_CVEID_list, path=NVD_CVEID_list_path)

if __name__ == '__main__':
    main()
    # compareItem('CVE-2004-0530')
    # compareItem('CVE-2010-1802')
    # chuliyixia()