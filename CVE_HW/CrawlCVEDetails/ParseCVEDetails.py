# -*- coding: utf-8 -*-

"""
Created on 2020-04-06 16:03  

@author: congyingxu
"""
from CommonFunction import JSONFIle_processing,File_processing
from CVE_HW.CompareDataset import CVEItemInfo
from CVE_HW import CONFIG
import urllib
import requests


CVEdetialsItems_dir = CONFIG.CVEdetialsItems_dir

def extractCVEdetailsItemInfo(CVEID):
    CVEdetialsItem = CVEItemInfo.CVEItem()

    CVEdetialsItem.ItemPath = CVEdetialsItems_dir + CVEID + '.json'
    Item_data = JSONFIle_processing.read(CVEdetialsItem.ItemPath)

    CVEdetialsItem.CVEID = CVEID

    CVEdetialsItem.Description = Item_data['desc']
    if Item_data['References'] == None:
        CVEdetialsItem.Reference = None
    else:
        # CVEdetialsItem.Reference = [ele.split(' ')[0] for ele in Item_data['References']]

        CVEdetialsItem.Reference = [urllib.parse.unquote(urllib.parse.unquote(ele.split(' ')[0])).replace('&amp;','&') for ele in Item_data['References']]
        # CVEdetialsItem.Reference = [ ele.replace('&amp;','&') for ele in CVEdetialsItem.Reference]

        if CVEdetialsItem.Reference != None:
            CVEdetialsItem.Reference = sorted(  CVEdetialsItem.Reference )

    # CVEdetialsItem.CVSS2 = ''
    # CVEdetialsItem.CVSS3 = ''
    # CVEdetialsItem.CVSS2Vector = ''
    # CVEdetialsItem.CVSS3Vector = ''
    CVEdetialsItem.CVSS2 = Item_data['CVSS Score'][0]


    # CVEdetialsItem.CWE = ''
    # CVEdetialsItem.AffectedVendorProductCPE = []
    # CVEdetialsItem.AffectedVendorProductVersionCPE = []
    CVEdetialsItem.CWE = 'CWE-' + Item_data['CWE ID'][0]
    if Item_data['CWE ID'][0] == 'CWE id is not defined for this vulnerability':
        CVEdetialsItem.CWE = None

    VP_list = []
    for node in Item_data['Affected Products'][1:]:
        if len(node) <2 :
            VP_list = None
        else:
            V = node[2].strip(' ')
            P = node[3].strip(' ')
            cpe = V + '__fdse__' + P
            VP_list.append(cpe.replace(' ','_').lower())
    if VP_list == None:
        CVEdetialsItem.AffectedVendorProductCPE = VP_list
    else:
        CVEdetialsItem.AffectedVendorProductCPE = sorted( set(VP_list) )

    # CVEdetialsItem.AffectedVendorProductVersionCPE = []
    # CVEdetialsItem.AffectedVendorProductVersionCPE = []
    VPV_record_list = []
    for VPV_ele in Item_data['Affected Products']:
        if VPV_ele[0] == '#' or VPV_ele[0] == '' or len(VPV_ele) <3:
            continue
        V = VPV_ele[2].strip(' ').lower().replace(' ', '_').strip('.0').replace('\\', '')
        P = VPV_ele[3].strip(' ').lower().replace(' ', '_').strip('.0').replace('\\', '')
        Version = VPV_ele[4].strip(' ').lower().replace(' ', '_').strip('.0').strip('.0').replace('\\', '')
        VPV_record = V + "__fdse__" + P + "__fdse__" + Version
        if '*' not in VPV_record and Version != '-' and len(Version) > 0:
            VPV_record_list.append(VPV_record)
    CVEdetialsItem.AffectedVendorProductVersionCPE = sorted(list(set(VPV_record_list)))
    if len( CVEdetialsItem.AffectedVendorProductVersionCPE ) == 0:
        CVEdetialsItem.AffectedVendorProductVersionCPE = None


    # CVEdetialsItem.OvalDefinition = []
    CVEdetialsItem.OvalDefinition = []
    if Item_data['OVAL Definitions'] != None:
        for ele in Item_data['OVAL Definitions']:
            Title = ele[0]
            DefinitionId = ele[1].split('__fdse__')[0].strip(' ')
            if Title == 'Title':
                continue
            CVEdetialsItem.OvalDefinition.append(DefinitionId)

        if len( CVEdetialsItem.OvalDefinition ) == 0:
            CVEdetialsItem.OvalDefinition = None
        else:
            CVEdetialsItem.OvalDefinition = sorted( list( set( CVEdetialsItem.OvalDefinition) ))
    else:
        CVEdetialsItem.OvalDefinition = None


    return CVEdetialsItem


def checkstorespace():
    path = '/Volumes/MyPassport/CVE/DataSet-NVD/NVDCpeRange/htmls/'
    print(len( File_processing.walk_FileDir(path) ))
    # path = '/Users/congyingxu/Downloads/CVE/'
    # print(len(File_processing.walk_FileDir(path)))

if __name__ == '__main__':

    # checkstorespace()
    print(extractCVEdetailsItemInfo('CVE-2011-3873').Reference)
    print(extractCVEdetailsItemInfo('CVE-2011-3873').OvalDefinition)