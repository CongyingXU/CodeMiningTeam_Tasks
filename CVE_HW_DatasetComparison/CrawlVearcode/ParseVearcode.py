# -*- coding: utf-8 -*-

"""
Created on 2020-04-08 13:31  

@author: congyingxu
"""

from CommonFunction import JSONFIle_processing, File_processing
from CVE_HW_DatasetComparison.CompareDataset import CVEItemInfo
from CVE_HW_DatasetComparison import CONFIG
import os
import urllib

VearcodeItems_dir = CONFIG.VearCodeItems_dir

VearcodeCVESID_map_path = CONFIG.VearcodeLanguageCVEVearcodeItemSID_map_path
VearcodeCVESID_map = JSONFIle_processing.read(VearcodeCVESID_map_path)



def extractVearcodeItemInfo(CVEID):

    VearcodeItem = CVEItemInfo.CVEItem()

    for language in VearcodeCVESID_map.keys():
        try:
            if CVEID in VearcodeCVESID_map[language].keys():
                if language not in VearcodeItem.Language:
                    VearcodeItem.Language += language + '__fdse__'

        except:
            continue
    VearcodeItem.Language = VearcodeItem.Language.strip('__fdse__')

    # VearcodeItemSID = 'sid-' + str( VearcodeCVESID_map[VearcodeItem.Language][CVEID][0] )
    # print(VearcodeItemSID)
    # if len( VearcodeCVESID_map[VearcodeItem.Language][CVEID] ) > 1:
    #     print("duplicate vearcode item:", CVEID, VearcodeCVESID_map[VearcodeItem.Language][CVEID])

    VearcodeItemSID_list = []
    for language in VearcodeItem.Language.split('__fdse__'):
        # print(SnykCVESID_map.keys())
        VearcodeItemSID_list.extend(VearcodeCVESID_map[language][CVEID])
        print("duplicate Snyk item:", CVEID, VearcodeCVESID_map[language][CVEID])

    # for VearcodeItemSID in VearcodeCVESID_map[VearcodeItem.Language][CVEID]:
    for VearcodeItemSID in VearcodeItemSID_list:
        VearcodeItemSID = 'sid-' + str( VearcodeItemSID )
        # print( VearcodeItemSID )
        ItemPath = VearcodeItems_dir + VearcodeItemSID +'.json'
        VearcodeItem.ItemPath += VearcodeItems_dir + VearcodeItemSID +'.json' +'__fdse__'
        Item_data = JSONFIle_processing.read(ItemPath)

        VearcodeItem.CVEID += CVEID + '__fdse__'
        VearcodeItem.Description += Item_data['overview'] + '__fdse__'

        if 'artifactLinks' not in Item_data.keys() and VearcodeItem.Reference == '':
            VearcodeItem.Reference = None
        elif VearcodeItem.Reference:
            VearcodeItem.Reference.extend([ ele['url']  for ele in Item_data['artifactLinks'] ] )
            VearcodeItem.Reference =  sorted( set( VearcodeItem.Reference  ))
        elif not VearcodeItem.AffectedVendorProductCPE:
            VearcodeItem.Reference = sorted(set([ ele['url']  for ele in Item_data['artifactLinks'] ]))

        if VearcodeItem.Reference and len( VearcodeItem.Reference ) ==0:
            VearcodeItem.Reference  = None
        if VearcodeItem.Reference:
            VearcodeItem.Reference = sorted( list( set(  VearcodeItem.Reference )) )

        # VearcodeItem.CVSS2 = ''
        # VearcodeItem.CVSS3 = ''
        # VearcodeItem.CVSS2Vector = ''
        # VearcodeItem.CVSS3Vector = ''
        if 'nvdCvssScore' in Item_data.keys():
            VearcodeItem.CVSS2 = str( Item_data['nvdCvssScore'] )
        else:
            VearcodeItem.CVSS2 = None


        if 'nvdCvssVector' in Item_data.keys():
            VearcodeItem.CVSS2Vector = Item_data['nvdCvssVector']
        else:
            VearcodeItem.CVSS2Vector = None


        VearcodeItem.CVSS3 = str( Item_data['nvdCvss3Score'] )
        VearcodeItem.CVSS3Vector = Item_data['nvdCvss3Vector']


        # VearcodeItem.CWE = ''
        # VearcodeItem.AffectedVendorProductCPE = []
        # VearcodeItem.AffectedVendorProductVersionCPE = []


        VP_list = []
        patch_list = []
        for node in Item_data['artifactComponents']:
            if node['coordTwo'] != None and len(node['coordTwo'])>0:
                coord = node['coordOne'] + '__fdse__' + node['coordTwo']
            else:
                coord = node['coordOne']
            # print(node['coordTwo'], coord)
            # # coord = coord.lower().strip('__fdse__')
            # print(node['coordTwo'], coord)
            coord = urllib.parse.unquote(urllib.parse.unquote(coord))
            VP_list.append(coord.lower().replace('.','_').replace('-','_'))
            # print(VP_list)

            for VR in node['versionRanges']:
                patch_link = VR['patch']
                if patch_link != None and patch_link !='':
                    patch_list.append(patch_link)

        if  VearcodeItem.AffectedVendorProductCPE == '' or not VearcodeItem.AffectedVendorProductCPE:
            VearcodeItem.AffectedVendorProductCPE = sorted(set(VP_list))
        elif  VearcodeItem.AffectedVendorProductCPE:
            VearcodeItem.AffectedVendorProductCPE.extend( VP_list )
            VearcodeItem.AffectedVendorProductCPE = sorted(set( VearcodeItem.AffectedVendorProductCPE ))
        if len( VearcodeItem.AffectedVendorProductCPE ) == 0:
            VearcodeItem.AffectedVendorProductCPE = None

        # print(patch_list)
        if not VearcodeItem.Patch or VearcodeItem.Patch == '':
            VearcodeItem.Patch = sorted(list(set(patch_list)) )
        elif VearcodeItem.Patch:
            VearcodeItem.Patch.extend( patch_list)
            VearcodeItem.Patch = sorted(list(set( VearcodeItem.Patch )) )

        # 数据清洗
        if VearcodeItem.Patch:
            patch_list_tem = []
            for ele in VearcodeItem.Patch:
                if len(ele.split('github.com/')) > 1:
                    # print(ele)
                    # print(VearcodeItem.Patch)
                    patch_list_tem.append('https://github.com/' + ele.split('github.com/')[1])
            VearcodeItem.Patch = patch_list_tem

        if len(VearcodeItem.Patch) == 0:
            VearcodeItem.Patch = None

        # VearcodeItem.AffectedVendorProductVersionCPE = []

    return VearcodeItem

if __name__ == '__main__':
    print( extractVearcodeItemInfo('CVE-2018-0770').AffectedVendorProductCPE )