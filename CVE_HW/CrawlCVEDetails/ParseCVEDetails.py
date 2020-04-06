# -*- coding: utf-8 -*-

"""
Created on 2020-04-06 16:03  

@author: congyingxu
"""
from CommonFunction import JSONFIle_processing,File_processing
from CVE_HW.CompareDataset import CVEItemInfo
from CVE_HW import CONFIG


CVEdetialsItems_dir = CONFIG.CVEdetialsItems_dir

def extractCVEdetailsItemInfo(CVEID):
    CVEdetialsItem = CVEItemInfo.CVEItem()

    CVEdetialsItem.ItemPath = CVEdetialsItems_dir + CVEID + '.json'
    Item_data = JSONFIle_processing.read(CVEdetialsItem.ItemPath)

    CVEdetialsItem.CVEID = CVEID

    CVEdetialsItem.Description = Item_data['cve']['description']['description_data'][0]['value']
    CVEdetialsItem.Reference = sorted([ele['url'] for ele in Item_data['references']['reference_data']])

    # CVEdetialsItem.CVSS2 = ''
    # CVEdetialsItem.CVSS3 = ''
    # CVEdetialsItem.CVSS2Vector = ''
    # CVEdetialsItem.CVSS3Vector = ''
    if 'baseMetricV2' in Item_data['impact'].keys():
        CVEdetialsItem.CVSS2 = Item_data['impact']['baseMetricV2']['cvssV2']['baseScore']
        CVEdetialsItem.CVSS2Vector = Item_data['impact']['baseMetricV2']['cvssV2']['vectorString']
    else:
        CVEdetialsItem.CVSS2 = None
        CVEdetialsItem.CVSS2Vector = None
    if 'baseMetricV3' in Item_data['impact'].keys():
        CVEdetialsItem.CVSS3 = Item_data['impact']['baseMetricV3']['cvssV3']['baseScore']
        CVEdetialsItem.CVSS3Vector = Item_data['impact']['baseMetricV3']['cvssV3']['vectorString']
    else:
        CVEdetialsItem.CVSS3 = None
        CVEdetialsItem.CVSS3Vector = None

    # CVEdetialsItem.CWE = ''
    # CVEdetialsItem.AffectedVendorProductCPE = []
    # CVEdetialsItem.AffectedVendorProductVersionCPE = []
    CVEdetialsItem.CWE = Item_data['cve']['problemtype']['problemtype_data'][0]['description'][0]['value']
    VP_list = []
    for node in Item_data['configurations']['nodes']:
        operation = node['operator']
        print(operation)
        cpe_match = node['cpe_match']
        for cpe_match_ele in cpe_match:
            cpe = cpe_match_ele['cpe23Uri'].split(':')[3] + '__fdse__' + cpe_match_ele['cpe23Uri'].split(':')[4]
            VP_list.append(cpe)
    CVEdetialsItem.AffectedVendorProductCPE = VP_list


def checkstorespace():
    path = '/Users/congyingxu/Downloads/CVE/DataSet-NVD/NVDCpeRange/htmls/'
    print(len( File_processing.walk_L1_FileNames(path) ))

checkstorespace()