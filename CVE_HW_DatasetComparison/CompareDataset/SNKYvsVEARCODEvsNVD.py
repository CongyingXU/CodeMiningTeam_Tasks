# -*- coding: utf-8 -*-

"""
Created on 2020-04-04 12:06

@author: congyingxu
"""

from CommonFunction import JSONFIle_processing
from CVE_HW_DatasetComparison.CrawlCVEDetails import ParseCVEDetails
from CVE_HW_DatasetComparison.CrawlerNVD import ParseNVD
from CVE_HW_DatasetComparison.CrawlSnyk import ParseSnyk
from CVE_HW_DatasetComparison.CrawlVearcode import ParseVearcode
from CVE_HW_DatasetComparison import CONFIG


CVE_CVEID_list_dir =  CONFIG.CVE_CVEID_list_dir
CVE_CVEID_list = sorted( JSONFIle_processing.read(CVE_CVEID_list_dir) )


NVDDataset_dir =  CONFIG.NVDDataset_dir
NVDYearDataset = {}
NVD_CVEID_list_path = CONFIG.NVD_CVEID_list_path
NVD_CVEID_list = JSONFIle_processing.read(NVD_CVEID_list_path)
NVDItems_dir = CONFIG.NVDItems_dir


# CVEDetails_CVEID_list_path = CONFIG.CVEDetails_CVEID_list_path
# CVEDetails_CVEID_list = JSONFIle_processing.read(CVEDetails_CVEID_list_path)
# CVEDetails_pages_dir = CONFIG.CVEDetails_pages_dir
# CVEDetailsItems_dir = CONFIG.SnykItems_dir

Snyk_LanguageItemSID_list_path = CONFIG.Snyk_LanguageItemSID_list_path
Snyk_LanguageCVESnykItemID_map_path = CONFIG.Snyk_LanguageCVESnykItemID_map_path

Snyk_LanguageItemSID_list = JSONFIle_processing.read(Snyk_LanguageItemSID_list_path)
Snyk_LanguageCVESnykItemID_map = JSONFIle_processing.read(Snyk_LanguageCVESnykItemID_map_path)

VearcodeCVESID_map_path = CONFIG.VearcodeLanguageCVEVearcodeItemSID_map_path
VearcodeCVESID_map = JSONFIle_processing.read(VearcodeCVESID_map_path)

VearcodeCVE_list = []
SnykCVE_list = []

differet_data_path = CONFIG.SnykvsVearcode_Different_path
differet_data = {'ComparedCVEIDs':[],'NotInVearcodeCVEIDs':[],'NotInSnykCVEIDs':[],'ComparedVearcodeCVEwithPatch':[],'ComparedSnykCVEwithPatch':[]}
differet_count  = 0



def compareItem(CVEID):
    global differet_count, differet_data, NVD_CVEID_list

    # # if CVEID exists in NVD
    # if CVEID not in SnykCVE_list or CVEID not in VearcodeCVE_list:
    #     print('-------------------------CVEID not in Snyk or not in Vearcode')
    #     return

    # if CVEID exists in NVD
    if CVEID not in SnykCVE_list:
        # print('-------------------------CVEID not in SnykCVE_list')
        # NotInNVDCVEIDs.append(CVEID)
        differet_data['NotInSnykCVEIDs'].append(CVEID)
        # return
    if CVEID not in VearcodeCVE_list:
        # print('-------------------------CVEID not in VearcodeCVE_list')
        # NotInCVEdetailsCVEIDs.append(CVEID)
        differet_data['NotInVearcodeCVEIDs'].append(CVEID)
        # return
    if CVEID not in SnykCVE_list or CVEID not in VearcodeCVE_list:
        return

    SnykItem = ParseSnyk.extractSnykItemInfo(CVEID)
    VearcodeItem = ParseVearcode.extractVearcodeItemInfo(CVEID)
    compareCVEInfo(SnykItem, VearcodeItem, CVEID)

    differet_data['ComparedCVEIDs'].append(CVEID)
    if SnykItem.Patch and len( SnykItem.Patch ) > 0:
        differet_data['ComparedSnykCVEwithPatch'].append(  CVEID)
    if VearcodeItem.Patch and len( VearcodeItem.Patch ) > 0:
        differet_data['ComparedVearcodeCVEwithPatch'].append(  CVEID)


def sameLanguage( Snyk_Language,  Vearcode_Language):
    for SnykItem_Language in Snyk_Language.split('__fdse__'):
        for VearcodeItem_Language in Vearcode_Language.split('__fdse__'):
            if SnykItem_Language == 'cocoapods' and VearcodeItem_Language == 'OBJECTIVEC':
                return True
            elif SnykItem_Language == 'rubygems' and VearcodeItem_Language == 'RUBY':
                return True
            elif SnykItem_Language == 'npm' and VearcodeItem_Language == 'JS':
                return True
            elif SnykItem_Language == 'JAVA' and VearcodeItem_Language == 'JAVA':
                return True
            elif SnykItem_Language == 'golang' and VearcodeItem_Language == 'GO':
                return True
            elif SnykItem_Language == 'composer' and VearcodeItem_Language == 'PHP':
                return True
            elif SnykItem_Language == 'nuget' and VearcodeItem_Language == 'CSHARP':
                return True
            elif SnykItem_Language == 'pip' and VearcodeItem_Language == 'PYTHON':
                return True

    return False


def compareCVEInfo(SnykItem, VearcodeItem, CVEID):
    global differet_count

    # compare: language types、reference、**patch / github commit、 Affected artifact/package、solution**
    field_num = 4
    flag = 0
    # Language
    if sameLanguage(SnykItem.Language, VearcodeItem.Language):
        # print('sssssssssssssame: Language')
        # print("CVEdetials_CVEID_desc", SnykItem.Language)
        # print("Vearcode_CVEID_desc", VearcodeItem.Language)

        pass
    else:
        flag = 1 * pow(10, field_num -1 )
        print('dddddddddddddifferent: Language')
        print("Snyk_CVEID_language", SnykItem.Language)
        print("Vearcode_CVEID_language", VearcodeItem.Language)
        pass

    # reference
    if SnykItem.Reference == VearcodeItem.Reference:
        # print('sssssssssssssame: reference')
        # print("nyk_CVEID_Reference", SnykItem.Reference)
        # print("Vearcode_CVEID_Reference", VearcodeItem.Reference)

        pass
    else:
        flag += 2 * pow(10, field_num -2 )
        print('dddddddddddddifferent: Reference')
        print("nyk_CVEID_Reference", SnykItem.Reference)
        print("Vearcode_CVEID_Reference",  VearcodeItem.Reference)
        pass

    # patch
    # print(SnykItem.Patch == VearcodeItem.Patch)
    if SnykItem.Patch == VearcodeItem.Patch:
        # print('sssssssssssssame: reference')
        # print("nyk_CVEID_CVSS2", SnykItem.CVSS2)
        # print("Vearcode_CVEID_CVSS2", VearcodeItem.CVSS2)

        pass
    else:
        flag += 3 * pow(10, field_num - 3)
        print('dddddddddddddifferent: Patch')
        print("Snyk_CVEID_Patch", SnykItem.Patch)
        print("Vearcode_CVEID_Patch", VearcodeItem.Patch)
        pass

    # Affected Vendor Product
    if SnykItem.AffectedVendorProductCPE == VearcodeItem.AffectedVendorProductCPE:
        # # print('sssssssssssssame: reference')
        # print("nyk_CVEID_AffectedVendorProductCPE", SnykItem.AffectedVendorProductCPE)
        # print("Vearcode_CVEID_AffectedVendorProductCPE", VearcodeItem.AffectedVendorProductCPE)

        pass
    else:
        flag += 4 * pow(10, field_num - 4)
        print('dddddddddddddifferent: AffectedVendorProductCPE')
        print("nyk_CVEID_AffectedVendorProductCPE", SnykItem.AffectedVendorProductCPE)
        print("Vearcode_CVEID_AffectedVendorProductCPE", VearcodeItem.AffectedVendorProductCPE)
        pass

    if flag != 0:
        print(flag)
        differet_count +=1
        differet_data[CVEID] = {}
        differet_data[CVEID]['flag'] = flag
        differet_data[CVEID]['Snyk'] = SnykItem.toDict()
        differet_data[CVEID]['Vearcode'] = VearcodeItem.toDict()






def main():
    global differet_count, differet_data, NVD_CVEID_list, VearcodeCVE_list, SnykCVE_list

    SnykCVE_list = []
    for language in Snyk_LanguageCVESnykItemID_map.keys():
        for key in Snyk_LanguageCVESnykItemID_map[language].keys():
            if key.startswith('CVE-'):
                SnykCVE_list.append(key)

    VearcodeCVE_list = []
    for language in VearcodeCVESID_map.keys():
        for key in VearcodeCVESID_map[language].keys():
            if key.startswith('CVE-'):
                VearcodeCVE_list.append(key)


    for CVEID in CVE_CVEID_list:
    # for CVEID in VearcodeCVE_list:
        # print(CVEID)
        # CVEID = 'CVE-2005-0834'
        # CVEID = 'CVE-2019-9865'
        # CVEID = 'CVE-2011-3871'
        compareItem(CVEID)
        # break

    JSONFIle_processing.write(json_content=differet_data , path=differet_data_path)
    print("differet_count: ", differet_count)
    print('SnykCVE_list: ', len(SnykCVE_list))
    print('VearcodeCVE_list: ', len(VearcodeCVE_list))


    # for CVEID in CVE_CVEID_list:
    # # for CVEID in VearcodeCVE_list:
    #     # print(CVEID)
    #     # CVEID = 'CVE-2005-0834'
    #     # CVEID = 'CVE-2019-9865'
    #     # CVEID = 'CVE-2011-3871'
    #     # CVEID = 'CVE-2011-4905'
    #     # CVEID = 'CVE-2013-1856'
    #     CVEID = 'CVE-2009-0580'
    #     compareItem(CVEID)
    #     break




# 写个方法，统计下 commit的数量
# Snyk:  JAVA 999
# Snyk:  pip 290
# Snyk:  nuget 90
# Snyk:  composer 209
# Snyk:  cocoapods 317
# Snyk:  npm 394
# Snyk:  rubygems 175
# Snyk:  golang 105

# Vearcode:  OBJECTIVEC 182
# Vearcode:  CPP 139
# Vearcode:  PHP 759
# Vearcode:  PYTHON 465
# Vearcode:  RUBY 307
# Vearcode:  GO 240
# Vearcode:  JS 500
# Vearcode:  JAVA 921
# Vearcode:  OS 192
# Vearcode:  CSHARP 270

def CollectCommitNum():
    SnykCVE_list = []
    SnykCVEPatch_list = {}
    for language in Snyk_LanguageCVESnykItemID_map.keys():
        for key in Snyk_LanguageCVESnykItemID_map[language].keys():
            if key.startswith('CVE-'):
                SnykCVE_list.append(key)
                SnykItem = ParseSnyk.extractSnykItemInfo(key)
                if SnykItem.Patch and SnykItem.Patch !=['']:
                    # print(SnykItem.Patch)

                    if language in SnykCVEPatch_list.keys():
                        SnykCVEPatch_list[language] += 1
                    else:
                        SnykCVEPatch_list[language] = 1




    VearcodeCVE_list = []
    VearcodeCVEPatch_list = {}
    for language in VearcodeCVESID_map.keys():
        for key in VearcodeCVESID_map[language].keys():
            if key.startswith('CVE-'):
                VearcodeCVE_list.append(key)
                VearcodeItem = ParseVearcode.extractVearcodeItemInfo(key)
                if VearcodeItem.Patch and VearcodeItem.Patch !=['']:
                    # print(VearcodeItem.Patch)

                    if language in VearcodeCVEPatch_list.keys():
                        VearcodeCVEPatch_list[language] += 1
                    else:
                        VearcodeCVEPatch_list[language] = 1

    # print()

    for language in SnykCVEPatch_list.keys():
        print("Snyk: ", language, SnykCVEPatch_list[language])
    for language in VearcodeCVEPatch_list.keys():
        print("Vearcode: ", language, VearcodeCVEPatch_list[language])


if __name__ == '__main__':
    main()
    # CollectCommitNum()