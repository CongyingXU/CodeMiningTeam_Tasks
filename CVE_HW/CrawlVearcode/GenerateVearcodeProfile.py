# -*- coding: utf-8 -*-

"""
Created on 2020-04-02 15:16

@author: congyingxu

用于h汇总Snky相关数据：
-SID Number
-Language Number & SID Number
-Meta-Module



。。。。
-CVE Number


Sid_Num 11221
os 2739
objective-c 719
go 540
ruby 680
java 1692
javascript 1859
cpp 640
csharp 350
python 910
php 1090
swift 2

"""
from CVE_HW.CrawlVearcode import VearcodeCrawler
from CVE_HW.CrawlSnyk import SnykItemCrawler,MavenCrawler
from CommonFunction import JSONFIle_processing

VearcodeItemUrlList_path ='/Users/congyingxu/Downloads/CVE/CrawledVearCodeHtmls/veracode_sid_url_list.json'

Profile_path = MavenCrawler.root_dir + "CVE/CrawledVearCodeHtmls/VearcodeDataSetProfile.json"
Profile = {}
sid_list = []
Language_data = {}

def Collect():
    VearcodeItemUrlList  = JSONFIle_processing.read(VearcodeItemUrlList_path)
    print("len( VearcodeItemUrlList)", len( VearcodeItemUrlList) )
    VearcodeItemUrlList = list( set(VearcodeItemUrlList) )
    print("len( VearcodeItemUrlList)", len(VearcodeItemUrlList))

    for ItemUrl in VearcodeItemUrlList:
        itemid = ItemUrl.split('/')[-2]
        type = ItemUrl.split('/')[-3]

        sid_list.append(itemid)
        if type in Language_data.keys():
            Language_data[type].append(itemid)
        else:
            Language_data[type] = [itemid]

    print('Sid_Num', len(sid_list))
    for type in Language_data.keys():
        print(type, len(Language_data[type]))

    # write
    Profile['VearcodeItemNumber'] = len(sid_list)
    # Meta-Mudule
    Profile['Meta-Module'] = ['links', 'community', 'priceInCents', 'disclosureDate', 'releasedDate', 'hasExploits', 'cweId', 'cvePublishedDate', 'cveLastModifiedDate', 'cve', 'id', 'createdDate', 'updatedDate', 'stage', 'title', 'overview', 'language', 'vulnerabilityTypes', 'nvdCvssScore', 'nvdCvssVector', 'nvdCvss3Score', 'nvdCvss3Vector', 'srcclrCvss3Score', 'srcclrCvss3Vector', 'artifactComponents', 'cveYear', 'cveDigits', 'cveStatus', 'artifactLinks', 'versionRangeMethods']
    Profile['Meta-Module'].extend(['versionRange', 'fixDate', 'patch','.....'])
    Profile['VearcodeTypeItems'] = []
    for type in Language_data.keys():
        Profile['VearcodeTypeItems'].append({type: len(Language_data[type])})
        # Profile['SnykTypes'][-1]['Numbers'] = len(Language_data[type])
        Profile['VearcodeTypeItems'][-1]['IDs'] = Language_data[type]

    JSONFIle_processing.write(Profile, Profile_path)


def getMetaModule():
    example_path = "/Users/congyingxu/Downloads/CVE/CrawledVearCodeHtmls/VearCodeItems/sid-506.json"
    example_item = JSONFIle_processing.read(example_path)

    print(example_item.keys())
    print(example_item['artifactComponents'][0].keys())



if __name__ == '__main__':
    Collect()
    # getMetaModule()