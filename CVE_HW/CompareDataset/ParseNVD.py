# -*- coding: utf-8 -*-

"""
Created on 2020-04-04 13:57  

@author: congyingxu
"""

from CommonFunction import JSONFIle_processing
from CVE_HW.CompareDataset import CVEItemInfo


NVDDataset_dir = "/Users/congyingxu/Downloads/CVE/DataSet-NVD/"
NVDYearDataset = {}
NVD_CVEID_list_path = "/Users/congyingxu/Downloads/CVE/MetaData/NVD_CVEID_list.json"
NVD_CVEID_list = JSONFIle_processing.read(NVD_CVEID_list_path)


NVDItems_dir = "/Users/congyingxu/Downloads/CVE/DataSet-NVD/NVDItems/"






def separateCVEItems():
    for year in range(2002,2021):
        file_path = NVDDataset_dir + "nvdcve-1.1-" + str(year) +'.json'
        year_dataset_content = JSONFIle_processing.read(file_path)

        # separate:
        CVE_Items = year_dataset_content['CVE_Items']
        for CVE_Item in CVE_Items:
            CVEID = CVE_Item['cve']['CVE_data_meta']['ID']
            print(CVEID)
            path = NVDItems_dir + CVEID +'.json'
            JSONFIle_processing.write(json_content=CVE_Item, path=path)
            # break


def extractNVDItemInfo(CVEID):

    NVDItem = CVEItemInfo.CVEItem()

    NVDItem.ItemPath = NVDItems_dir + CVEID +'.json'
    Item_data = JSONFIle_processing.read(NVDItem.ItemPath)

    NVDItem.CVEID = CVEID
    NVDItem.Description = Item_data['cve']['description']['description_data'][0]['value']
    NVDItem.Reference =   sorted( [ ele['url']  for ele in Item_data['references']['reference_data'] ] )

    # NVDItem.CVSS2 = ''
    # NVDItem.CVSS3 = ''
    # NVDItem.CVSS2Vector = ''
    # NVDItem.CVSS3Vector = ''
    if 'baseMetricV2' in Item_data['impact'].keys():
        NVDItem.CVSS2 = Item_data['impact']['baseMetricV2']['cvssV2']['baseScore']
        NVDItem.CVSS2Vector = Item_data['impact']['baseMetricV2']['cvssV2']['vectorString']
    else:
        NVDItem.CVSS2 = None
        NVDItem.CVSS2Vector = None
    if 'baseMetricV3' in Item_data['impact'].keys():
        NVDItem.CVSS3 = Item_data['impact']['baseMetricV3']['cvssV3']['baseScore']
        NVDItem.CVSS3Vector = Item_data['impact']['baseMetricV3']['cvssV3']['vectorString']
    else:
        NVDItem.CVSS3 = None
        NVDItem.CVSS3Vector = None

    # NVDItem.CWE = ''
    # NVDItem.AffectedVendorProductCPE = []
    # NVDItem.AffectedVendorProductVersionCPE = []
    NVDItem.CWE = Item_data['cve']['problemtype']['problemtype_data'][0]['description'][0]['value']
    VP_list = []
    for node in Item_data['configurations']['nodes']:
        operation = node['operator']
        print(operation)
        cpe_match = node['cpe_match']
        for cpe_match_ele in cpe_match:
            cpe = cpe_match_ele['cpe23Uri'].split(':')[3] + '__fdse__' + cpe_match_ele['cpe23Uri'].split(':')[4]
            VP_list.append(cpe)
    NVDItem.AffectedVendorProductCPE = VP_list





if __name__ == '__main__':
    separateCVEItems()

