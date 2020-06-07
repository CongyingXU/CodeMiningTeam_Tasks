# -*- coding: utf-8 -*-

"""
Created on 2020-04-04 13:57  

@author: congyingxu

CVE-2014-2925 Pass, to check,  len(tr[class]) == 0  !
CVE-2011-0395 Pass, to check,  len(tr[class]) == 0  !
CVE-2014-1902 Pass, to check,  len(tr[class]) == 0  !

CVE-2019-12220 ['AND']
CVE-2004-1416 ['OR']
CVE-2010-1802 ['AND', 'OR', 'OR']
"""

from CommonFunction import JSONFIle_processing, File_processing
from CVE_HW.CompareDataset import CVEItemInfo
from CVE_HW import CONFIG
import os
from bs4 import BeautifulSoup
import urllib

NVDDataset_dir = CONFIG.NVDDataset_dir
NVDYearDataset = {}
NVD_CVEID_list_path = CONFIG.NVD_CVEID_list_path
NVD_CVEID_list = JSONFIle_processing.read(NVD_CVEID_list_path)

NVDItems_dir = CONFIG.NVDItems_dir
NVDCperange_html_dir = CONFIG.NVDCperange_html_dir
NVDCperange_items_dir = CONFIG.NVDCperange_items_dir

NVD_NoCpeRange_list_path = CONFIG.NVD_NoCpeRange_list_path
NVD_NoCpeRange_list = JSONFIle_processing.read(NVD_NoCpeRange_list_path)

NVD_CpeANDOR_list_path = CONFIG.NVD_CpeANDOR_list_path
NVD_CpeANDOR_list = JSONFIle_processing.read(NVD_CpeANDOR_list_path)

NVD_CpeRange_items_dir = CONFIG.NVD_CpeRange_items_dir

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





def parserNVDCpeRangeHtml(html,CVEID):
    global  NVD_NoCpeRange_list, NVD_NoCpeRange_list_path , NVD_CpeANDOR_list, NVD_CpeANDOR_list_path

    CpeRange_data ={}
    soup = BeautifulSoup(html, 'lxml')

    # Configuration: cpe_list , running on / with
    id_num = 1
    # 针对每个confiug
    while soup.find(id = 'config-div-' + str(id_num)) != None:
        CpeConfig_data = {}
        div =  soup.find(id = 'config-div-' + str(id_num))
        trs = div.find_all('tr')

        # print(div.contents[1].name, div.contents[1]['class'])
        if div.contents[1].name == 'span' and div.contents[1]['class'] ==  ['badge']:  # and or 模式
            NVD_CpeANDOR_list.append(CVEID)
            JSONFIle_processing.write(json_content=list(set(NVD_CpeANDOR_list)), path=NVD_CpeANDOR_list_path)

            # find span， judge wether 1 AND and other OR
            spans = div.find_all('span', attrs = {'class':'badge'})
            spans_list = []
            span_count = 0 # 用于区别 AND、OR, 同时，如果 >1 则是两层结构，否则，就是一层结构
            value = '' # 用于标记当前 AND、OR
            level1_value = '' # 用于记录第一层的值
            # for span in spans:
            #     spans_list.append(span.text.replace('\n','').strip('\n').strip('\t').strip('  '))
            # print(CVEID, spans_list)

            for index in range(len(div.contents)):
                content = div.contents[index]
                if content.name == 'span' and span_count== 0: # 说明还在第一层
                    value = content.text.replace('\n','').strip('\n').strip('\t').strip('  ') + str(span_count)
                    level1_value = value
                    span_count += 1

                    CpeConfig_data[value] = {}
                elif  content.name == 'span' and span_count> 0: # s说明已经在第二层了
                    value = content.text.replace('\n', '').strip('\n').strip('\t').strip('  ') + str(span_count)
                    span_count += 1
                    CpeConfig_data[level1_value][value] = [] # 如果有第二层，那么第一层一定是 AND; No, 不一定，比如：CVE-2015-1188

                if content.name == 'table' and span_count== 1 and value != '' : # 说明只有一层 AND OR, value == ''  说明是空的table
                    CpeConfig_data[value] = []
                    table = content
                    trs = table.find_all('tr')
                    for tr in trs:  # 针对每个条目，如：running on/with
                        tds = tr.find_all('td')  # cpe title

                        CpeConfig_data[value].append({ })  # VP xixni
                        for td in tds:
                            cpetitle = td.find('b').text.replace('\n', '').strip('\n').strip('\t').strip('  ')
                            CpeConfig_data[value][-1][cpetitle] = []   # VP xixni

                            lis = td.find_all('li')
                            for li in lis:
                                if li.find('li') != None:  # 说明是被删除过，这个就不统计了，更新后信息在下一个li中
                                    continue

                                cpedetail = li.text.replace('\n', '').strip('\n').strip('\t').strip('  ')
                                CpeConfig_data[value][-1][cpetitle].append(cpedetail)  # 具体VPV 信息
                    value = '' # 该 AND OR 已经用过了
                elif content.name == 'table' and span_count> 1 and value != '' : # 说明是两层 AND OR
                    table = content
                    trs = table.find_all('tr')
                    for tr in trs:  # 针对每个条目，如：running on/with
                        tds = tr.find_all('td')  # cpe title

                        CpeConfig_data[level1_value][value].append({})
                        for td in tds:
                            cpetitle = td.find('b').text.replace('\n', '').strip('\n').strip('\t').strip('  ')
                            CpeConfig_data[level1_value][value][-1][cpetitle] = []  # VP xixni

                            lis = td.find_all('li')
                            for li in lis:
                                if li.find('li') != None:  # 说明是被删除过，这个就不统计了，更新后信息在下一个li中
                                    continue

                                cpedetail = li.text.replace('\n', '').strip('\n').strip('\t').strip('  ')
                                CpeConfig_data[level1_value][value][-1][cpetitle].append(cpedetail)  # 具体VPV 信息
                    value = ''  # 该 AND OR 已经用过了

            # print(CVEID, 'Pass, to check,  len(tr[class]) == 0  !')
            # return 'Pass'

        else: # class 模式
            for tr in trs:  # 针对每个条目，如：running on/with
                # to check
                if len(tr['class']) > 1:
                    print(CVEID, 'to check,  len(tr[class]) > 1 !')

                class_str = tr['class'][0]
                if class_str not in CpeConfig_data.keys():
                    CpeConfig_data[class_str] = []     # class title 信息

                tds = tr.find_all('td') # cpe title
                CpeConfig_data[class_str].append({})
                for td in tds:
                    cpetitle = td.find('b').text.replace('\n','').strip('\n').strip('\t').strip('  ')
                    CpeConfig_data[class_str][-1][cpetitle] = []   # VP xixni

                    lis = td.find_all('li')
                    for li in lis:
                        if li.find('li') != None: # 说明是被删除过，这个就不统计了，更新后信息在下一个li中
                            continue

                        cpedetail = li.text.replace('\n','').strip('\n').strip('\t').strip('  ')
                        CpeConfig_data[class_str][-1][cpetitle].append(cpedetail)  # 具体VPV 信息


        CpeRange_data['config-'+str(id_num)] = CpeConfig_data
        id_num +=1

    # to check
    if id_num == 1:
        print("Pass, id_num == 1, Check!! no cpe range")
        NVD_NoCpeRange_list.append(CVEID)
        JSONFIle_processing.write(json_content=list(set(NVD_NoCpeRange_list)) , path=NVD_NoCpeRange_list_path)
        return 'Pass'

    return CpeRange_data

def parserNVDCpeRangeInfo():
    for CVEID in NVD_CVEID_list:
        # CVEID = 'CVE-2015-1188'
        # CVE-2019-12220 ['AND']
        # CVE-2004-1416 ['OR']
        # CVE-2012-1844
        # CVE-2014-2925
        # CVE-2010-1802 ['AND', 'OR', 'OR']
        print(CVEID)
        html_file_path = NVDCperange_html_dir + CVEID + '.html'
        item_file_path = NVDCperange_items_dir + CVEID + '.json'
        if os.path.exists(item_file_path):
                continue

        html = File_processing.read_TXTfile(html_file_path)
        CpeRange_data = parserNVDCpeRangeHtml(html,CVEID)
        # print(item_file_path)
        if CpeRange_data == 'Pass':
            continue
        JSONFIle_processing.write(json_content=CpeRange_data, path = item_file_path)
        # break


def extractNVDItemInfo(CVEID):

    NVDItem = CVEItemInfo.CVEItem()

    NVDItem.ItemPath = NVDItems_dir + CVEID +'.json'
    Item_data = JSONFIle_processing.read(NVDItem.ItemPath)

    NVDItem.CVEID = CVEID
    NVDItem.Description = Item_data['cve']['description']['description_data'][0]['value']
    # NVDItem.Reference =   sorted( [ ele['url']  for ele in Item_data['cve']['references']['reference_data'] ] )

    ReferenceList = []
    OVALList = []
    for ele in Item_data['cve']['references']['reference_data']:
        url = urllib.parse.unquote(urllib.parse.unquote(ele['url'])).replace('&amp;','&')
        src = ele['url']
        name = ele['name']
        if '/oval.' in url or  src == 'OVAL':
            OVALList.append(name)
        else:
            ReferenceList.append(url)

    NVDItem.Reference = sorted( list( set( ReferenceList ) ) )
    NVDItem.OvalDefinition = sorted(list(set(OVALList)))

    if len( NVDItem.Reference ) ==0:
        NVDItem.Reference  = None
    if len(NVDItem.OvalDefinition) == 0:
        NVDItem.OvalDefinition = None

    # NVDItem.CVSS2 = ''
    # NVDItem.CVSS3 = ''
    # NVDItem.CVSS2Vector = ''
    # NVDItem.CVSS3Vector = ''
    if 'baseMetricV2' in Item_data['impact'].keys():
        NVDItem.CVSS2 = str( Item_data['impact']['baseMetricV2']['cvssV2']['baseScore'] )
        NVDItem.CVSS2Vector = Item_data['impact']['baseMetricV2']['cvssV2']['vectorString']
    else:
        NVDItem.CVSS2 = None
        NVDItem.CVSS2Vector = None
    if 'baseMetricV3' in Item_data['impact'].keys():
        NVDItem.CVSS3 = str( Item_data['impact']['baseMetricV3']['cvssV3']['baseScore'] )
        NVDItem.CVSS3Vector = Item_data['impact']['baseMetricV3']['cvssV3']['vectorString']
    else:
        NVDItem.CVSS3 = None
        NVDItem.CVSS3Vector = None

    # NVDItem.CWE = ''
    # NVDItem.AffectedVendorProductCPE = []
    # NVDItem.AffectedVendorProductVersionCPE = []
    try:
        NVDItem.CWE = Item_data['cve']['problemtype']['problemtype_data'][0]['description'][0]['value']
    except IndexError:
        NVDItem.CWE = None
    if NVDItem.CWE == 'NVD-CWE-noinfo' or NVDItem.CWE == 'NVD-CWE-Other':
        NVDItem.CWE = None

    VP_list = []
    for node in Item_data['configurations']['nodes']:
        operation = node['operator']
        # print(operation)
        if 'children' in node.keys():
            children = node['children']
            for ele in children:
                cpe_match = ele['cpe_match']
                for cpe_match_ele in cpe_match:
                    if cpe_match_ele['vulnerable'] :
                        cpe = cpe_match_ele['cpe23Uri'].split(':')[3] + '__fdse__' + cpe_match_ele['cpe23Uri'].split(':')[4]
                        VP_list.append(cpe.replace('\\', '').strip('_'))
        else:
            cpe_match = node['cpe_match']
            for cpe_match_ele in cpe_match:
                if cpe_match_ele['vulnerable']:
                    cpe = cpe_match_ele['cpe23Uri'].split(':')[3] + '__fdse__' + cpe_match_ele['cpe23Uri'].split(':')[4]
                    VP_list.append(cpe.replace('\\', '').strip('_'))
    NVDItem.AffectedVendorProductCPE = sorted(set(VP_list))
    if len( NVDItem.AffectedVendorProductCPE ) == 0:
        NVDItem.AffectedVendorProductCPE = None


    # NVDItem.AffectedVendorProductVersionCPE = []
    VPV_record_list = []
    CpeRange_item_path = NVD_CpeRange_items_dir + CVEID + '.json'
    if os.path.exists(CpeRange_item_path):

        CpeRange_item_info = JSONFIle_processing.read(CpeRange_item_path)
        for config in CpeRange_item_info.keys():
            config_info = CpeRange_item_info[config]
            if 'vulnerable' in config_info.keys():
                vuln_config_info = config_info['vulnerable']
                NVDItem.tag_ANDOR = False
            else: ### AND OR 未处理
                NVDItem.tag_ANDOR = True
                continue
            for record in vuln_config_info:
                for VP_key in record.keys():
                    if ':' not in VP_key or ':*' not in VP_key: # 说明是： Up to (including)1.5， 这类信息
                        NVDItem.tag_CpeRange = True
                        continue
                    V  = VP_key.split(':')[3].strip(' ').lower().replace(' ','_').strip('.0').replace('\\', '').strip('_')
                    P = VP_key.split(':')[4].strip(' ').lower().replace(' ', '_').strip('.0').replace('\\', '').strip('_')
                    Version = VP_key.split(':')[5].strip(' ').lower().replace(' ', '_').strip('.0').replace('\\', '')
                    VPV_record = V + "__fdse__" + P + "__fdse__" + Version
                    if '*' not in VPV_record and Version != '-' and len(Version) > 0:
                        VPV_record_list.append(VPV_record)


                    for VPV_ele in record[VP_key]:
                        V = VPV_ele.split(':')[3].strip(' ').lower().replace(' ', '_').strip('.0').replace('\\', '').strip('_')
                        P = VPV_ele.split(':')[4].strip(' ').lower().replace(' ', '_').strip('.0').replace('\\', '').strip('_')
                        Version = VPV_ele.split(':')[5].strip(' ').lower().replace(' ', '_').strip('.0').replace('\\', '')
                        VPV_record = V + "__fdse__" + P + "__fdse__" + Version
                        if '*' not in VPV_record and Version != '-' and len(Version) > 0:
                            VPV_record_list.append(VPV_record)

        NVDItem.AffectedVendorProductVersionCPE = sorted( list( set( VPV_record_list ) ) )

        if len(NVDItem.AffectedVendorProductVersionCPE) == 0:
            NVDItem.AffectedVendorProductVersionCPE = None
    else:
        NVDItem.AffectedVendorProductVersionCPE = None
        print(CVEID,"To check: NVDItem.AffectedVendorProductVersionCPE = None")


    return NVDItem





if __name__ == '__main__':
    # separateCVEItems() # 从导出的NVD feed中数据，将每个NVD信息分割开
    # parserNVDCpeRangeInfo() # 解析出每个CpeRange的信息
    # print( extractNVDItemInfo('CVE-2011-3873').Reference )
    print(extractNVDItemInfo('CVE-2004-2241').AffectedVendorProductVersionCPE)

