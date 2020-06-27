# -*- coding: utf-8 -*-

"""
Created on 2020-04-02 14:41  

@author: congyingxu

用于收集Vearcode 平台漏洞item数据，以及提取出CVE相关数据
"""



from CVE_HW_DatasetComparison.CrawlVearcode import VearcodeCrawler
from CVE_HW_DatasetComparison.CrawlSnyk import SnykItemCrawler,MavenCrawler
from CommonFunction import JSONFIle_processing,File_processing

VearcodeItem_dir ='/Users/congyingxu/Downloads/CVE/CrawledVearCodeHtmls/VearCodeItems/'
Profile_path = MavenCrawler.root_dir + "CVE/CrawledVearCodeHtmls/VearcodeDataSetProfile.json"
Profile = JSONFIle_processing.read(Profile_path)

VearcodeItemSIDData_path = '/Users/congyingxu/Downloads/CVE/CrawledVearCodeHtmls/VearcodeItemSIDData.json'
VearcodeItemSIDData = {}

VearcodeItemCVEData_path = '/Users/congyingxu/Downloads/CVE/CrawledVearCodeHtmls/VearcodeItemCVEData.json'
VearcodeItemCVEData = {}

None_CVE  = 0
Existing_CVE = 0

def extractiteminfo(file_path):
    global VearcodeItemCVEData, None_CVE, Existing_CVE, VearcodeItemSIDData

    SID_content = JSONFIle_processing.read(file_path)

    # 对应语言
    Language = SID_content['language']
    if Language not in VearcodeItemCVEData.keys():
        VearcodeItemCVEData[Language] = {}
        VearcodeItemSIDData[Language] = []
        VearcodeItemCVEData[Language]["SIDNumber"] = 0
    else:
        pass

    # 提取CVE_ID，VearcodeItemCVEData信息
    SID = SID_content['id']
    VearcodeItemSIDData[Language].append(SID)



    # 对应CVE
    if SID_content['cve'] == None:
        None_CVE +=1
        return

    # 提取CVE_ID，VearcodeItemCVEData信息
    SID = SID_content['id']
    CVE_ID = "CVE-" + SID_content['cve']
    if CVE_ID not in VearcodeItemCVEData[Language].keys():
        VearcodeItemCVEData[Language][CVE_ID] = [SID]
    else:
        VearcodeItemCVEData[Language][CVE_ID].append( SID )
        print("Existing :", CVE_ID, SID, VearcodeItemCVEData[Language][CVE_ID])
        Existing_CVE +=1

    VearcodeItemCVEData[Language]["SIDNumber"] = VearcodeItemCVEData[Language]["SIDNumber"] + 1





    # 验证SID-CVE无一对多的问题
    # if CVE_ID != None and len(SID_content['cve']) > 15:
    #     print(SID_content['cve'])





def main():
    global VearcodeItemCVEData

    file_names = File_processing.walk_L1_FileNames(VearcodeItem_dir)
    print(len( file_names ))
    for file_name in file_names:
        if file_name.endswith('.DS_Store'):
            continue

        file_path = VearcodeItem_dir + file_name
        extractiteminfo(file_path)


    # write
    JSONFIle_processing.write(VearcodeItemCVEData,VearcodeItemCVEData_path)
    JSONFIle_processing.write(VearcodeItemSIDData,VearcodeItemSIDData_path)

    print(VearcodeItemCVEData.keys())
    SID_Count = 0
    CVE_count = 0
    for language in VearcodeItemCVEData.keys():

        print("VearcodeItemSIDData", language, len( VearcodeItemSIDData[language] ))
        print("VearcodeItemCVEData",language, len( VearcodeItemCVEData[language] )-1 ,  VearcodeItemCVEData[language]["SIDNumber"] )
        CVE_count += len( VearcodeItemCVEData[language] )-1
        SID_Count += VearcodeItemCVEData[language]["SIDNumber"]

    print("SID_Count",SID_Count)
    print("CVE_count", CVE_count)

    print("None_CVE",None_CVE)
    print("Existing_CVE", Existing_CVE)


if __name__ == '__main__':
    main()


