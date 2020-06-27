# -*- coding: utf-8 -*-

"""
Created on 2020-04-04 13:57

@author: congyingxu
1、parseSnkyItempages: 用于将爬取的html 解析成 JSON Item
基本信息包括：

Title
Affected package & Vesion
Overview
Details ：PoC by snyk有代码信息，json不太好存
Types of attacks
Affected environments
How to prevent
Remediation
Reference
Patch: from Reference Github commit / other forms?

Snyk patch available for versions: npm__call__20160705

CVSS Score & Vector

Credit ? is the same as CVE's contibutor
CVE
CWE
SNYK-ID
Disclosed Date
Published Data



SNYK-JAVA-ORGECLIPSEJETTYAGGREGATE-31118 to check no Overview.
npm:360class.jansenhm:20170617 Title == None
npm:11xiaoli:20170509 Title == None
SNYK-PHP-CROOGOCROOGO-72033 to check no Overview.
SNYK-RUBY-WEBCONSOLE-20196 cvss_div==None
npm:22lixian:20170511 Title == None
npm:626:20180226 Title == None


Snyk_LanguageCVESnykItemID_map JAVA 2080 2969
Snyk_LanguageCVESnykItemID_map pip 708 764
Snyk_LanguageCVESnykItemID_map nuget 390 560
Snyk_LanguageCVESnykItemID_map composer 704 916
Snyk_LanguageCVESnykItemID_map cocoapods 679 744
Snyk_LanguageCVESnykItemID_map npm 941 1041
Snyk_LanguageCVESnykItemID_map rubygems 449 475
Snyk_LanguageCVESnykItemID_map golang 129 163
Snyk_LanguageItemSID_list JAVA 3513
Snyk_LanguageItemSID_list pip 1037
Snyk_LanguageItemSID_list nuget 673
Snyk_LanguageItemSID_list composer 1355
Snyk_LanguageItemSID_list cocoapods 744
Snyk_LanguageItemSID_list npm 2141
Snyk_LanguageItemSID_list rubygems 683
Snyk_LanguageItemSID_list golang 207

Snyk_LanguageCVESnykItemID_map JAVA 2150 3079
Snyk_LanguageCVESnykItemID_map pip 713 770
Snyk_LanguageCVESnykItemID_map nuget 421 591
Snyk_LanguageCVESnykItemID_map composer 708 920
Snyk_LanguageCVESnykItemID_map cocoapods 680 746
Snyk_LanguageCVESnykItemID_map npm 980 1083
Snyk_LanguageCVESnykItemID_map rubygems 459 486
Snyk_LanguageCVESnykItemID_map golang 131 165
Snyk_LanguageItemSID_list JAVA 3513
Snyk_LanguageItemSID_list pip 1037
Snyk_LanguageItemSID_list nuget 673
Snyk_LanguageItemSID_list composer 1355
Snyk_LanguageItemSID_list cocoapods 744
Snyk_LanguageItemSID_list npm 2141
Snyk_LanguageItemSID_list rubygems 683
Snyk_LanguageItemSID_list golang 207

"""

from CommonFunction import JSONFIle_processing, File_processing
from CVE_HW_DatasetComparison.CompareDataset import CVEItemInfo
from CVE_HW_DatasetComparison import CONFIG
import os
from bs4 import BeautifulSoup
import urllib


SnykItems_dir = CONFIG.SnykItems_dir
SnykItemspages_dir = CONFIG.Snyk_ItemPages_dir
Snyk_LanguageItemSID_list_path = CONFIG.Snyk_LanguageItemSID_list_path
Snyk_LanguageCVESnykItemID_map_path = CONFIG.Snyk_LanguageCVESnykItemID_map_path

Snyk_LanguageItemSID_list = JSONFIle_processing.read(Snyk_LanguageItemSID_list_path)
Snyk_LanguageCVESnykItemID_map = JSONFIle_processing.read(Snyk_LanguageCVESnykItemID_map_path)


Snyk_ItemID_list_path = CONFIG.Snyk_ItemID_list_path
Snyk_ItemID_list = JSONFIle_processing.read(Snyk_ItemID_list_path)


def parseSnkyItemsPages():
    for SnykID in Snyk_ItemID_list:
        print(SnykID)
        # SnykID = 'npm:closurecompiler:20160831'
        # SnykID = 'npm:360class.jansenhm:20170617'
        # SnykID = 'SNYK-RUBY-WEBCONSOLE-20196'
        # SnykID = 'SNYK-JAVA-ORGWEBJARSNPM-479548'
        # SnykID = 'npm:call:20160705'
        # SnykID = 'npm:libnotify:20130515'
        itempage_path = SnykItemspages_dir + SnykID.replace(':','__') + '.html'
        SnykitemInfo_path = SnykItems_dir + SnykID.replace(':', "__") + '.json'
        # if os.path.exists(SnykitemInfo_path):
        #     continue

        html = File_processing.read_TXTfile(itempage_path)
        SnykitemInfo = parseSnykHtml(html,SnykID)

        JSONFIle_processing.write(json_content=SnykitemInfo, path=SnykitemInfo_path)
        # break

def parseSnykHtml(html,SnykID):
    soup = BeautifulSoup(html, 'lxml')
    item_info = {}

    # Title
    Title_span = soup.find('span',attrs={'class':'header__title__text'})
    if Title_span == None:
        print(SnykID, "Title == None")
        return item_info
    else:
        Title = Title_span.text

    # Affected package & Vesion
    header__p = soup.find('p',attrs={"class":'header__lede'})
    strongs = header__p.find_all('strong')
    # print(header__p)
    # print(strongs)
    # to check
    if len(strongs) > 2:
        print('to check, len(strongs) > 2')
    try: # 因为有的没有link，咩有 a
        Affected_product = strongs[0].a['href'].split(':')[-1]
        Language = strongs[0].a['href'].split('/')[-1].split(':')[0]
    except TypeError:
        Affected_product = strongs[0].text.replace('\n','').strip('\n').strip('\t').strip('            ')
        if ':' in SnykID:
            Language = SnykID.split(':')[0]
        else:
            Language = SnykID.split('-')[1]
    if len( strongs) >1 :
        Affected_version = strongs[1].text
    else:
        Affected_version = None

    item_info['Title'] = Title
    item_info['Affected_product'] = Affected_product
    item_info['Language'] = Language
    item_info['Affected_version'] = Affected_version


    # CVSS Score & Vector
    #
    # Credit ? is the same as CVE's contibutor
    # CVE
    # CWE
    # SNYK-ID
    # Disclosed Date
    # Published Data

    cvss_div = soup.find('div',attrs={'class':'cvss-breakdown'})
    if cvss_div!=None :
        CVSS_Score = cvss_div.header.find('div').find('div').text
        cvss_breakdown__items = cvss_div.find('ul', attrs = {'class':'cvss-breakdown__items'})
        CVSS_Vector  = {}
        for li in cvss_breakdown__items.find_all('li'):
            cvss_breakdown__title = li.find('div',attrs = {'class':'cvss-breakdown__title'}).text
            cvss_breakdown__desc = li.find('div',attrs = {'class':'cvss-breakdown__desc'}).text
            CVSS_Vector[cvss_breakdown__title] = cvss_breakdown__desc
        item_info['CVSS_Score'] = CVSS_Score
        item_info['CVSS_Vector'] = CVSS_Vector
    else:
        print(SnykID, 'cvss_div==None')
        item_info['CVSS_Score'] = None
        item_info['CVSS_Vector'] = None

    div_vuln = soup.find('div', attrs={'class':'vuln-sidebar-offset'})
    if div_vuln == None:
        div_vuln = soup.find('div', attrs={'class': 'card card--sidebar'})
        card__content = div_vuln.find_all('div', attrs = {'class':'card__content'})[0]
        # print(len( soup.find_all('div', attrs = {'class':'card__content'})))
    else:
        card__content = div_vuln.find_all('div', attrs = {'class':'card__content'})[1]
    dl = card__content.find('dl')
    dt = ''
    for index in range( len(dl.contents) ):
        content = dl.contents[index]
        if content.name == 'dt':
            dt = content.text.replace('\n','').strip('\n').strip('\t').strip('            ')
        elif content.name == 'dd' and dt != '':
            dd =  dl.contents[index].text.replace('\n','').strip('\n').strip('\t').strip('            ')
            item_info[dt] = dd




    # Overview
    # Details ：PoC by snyk有代码信息，json不太好存
    # Types of attacks
    # Affected environments
    # How to prevent
    # Remediation
    # Reference
    # Patch: from Reference Github commit / other forms?

    item_info['Patch'] = []
    div_prose  = soup.find('div',attrs = {'class':'prose'})
    div = div_prose.find('div', attrs={'class': 'card__content'})
    fiels_name = ''
    field_value = ''
    for index in range(len(div.contents)):
        content = div.contents[index]
        if content.name == 'h2' or content.name == 'h3':
            fiels_name = content['id']
            field_value = ''

            # fiels_name == 'snyk-patches' 特殊处理：
            if fiels_name == 'snyk-patches':
                item_info[fiels_name] = []
                for li in content.find_all('li'):
                    url_title = li.text.replace('\n', '').strip('\n').strip('\t').strip('            ')
                    try:
                        url = li.a['href']
                    except TypeError:
                        continue
                    full_url = url_title + '__fdse__' + url
                    item_info[fiels_name].append(full_url)

                    # patch
                    if 'commit' in url_title.lower() or '/commit/' in url:
                        item_info['Patch'].append(url)
                        item_info['Patch'] = list(set(item_info['Patch']))
        elif content.name == 'ul' and ( fiels_name == 'references' or fiels_name == 'snyk-patches'): # npm__call__20160705
            item_info[fiels_name] = []
            for li in content.find_all('li'):
                url_title = li.text.replace('\n', '').strip('\n').strip('\t').strip('            ')
                try:
                    url = li.a['href']
                except TypeError:
                    continue
                full_url = url_title + '__fdse__' + url
                item_info[fiels_name].append(full_url)

                # patch
                if 'commit' in url_title.lower() or '/commit/' in url:
                    item_info['Patch'].append(url)
                    item_info['Patch'] = list( set( item_info['Patch'] ) )
        elif content.name == 'p' and fiels_name == 'references': # for SNYK-JAVA-ORGWEBJARSNPM-479548
            item_info[fiels_name] = []
            for a in content.find_all('a'):
                url_title = a.text.replace('\n', '').strip('\n').strip('\t').strip('            ')
                try:
                    url = a['href']
                except TypeError:
                    continue
                full_url = url_title + '__fdse__' + url
                item_info[fiels_name].append(full_url)

                # patch
                if 'commit' in url_title.lower() or '/commit/' in url:
                    item_info['Patch'].append(url)
        elif  ( content.name != 'h2' and content.name and fiels_name != '' ) or (content.name == 'ul' and fiels_name != 'references'):
            # print(content.name)
            field_value += content.text
            item_info[fiels_name] = field_value


        elif content.name == None:
            pass
        elif content.name == 'p' and fiels_name =='' and 'overview' not in item_info.keys():
            fiels_name = 'overview'
            field_value += content.text
            item_info[fiels_name] = field_value
            print(SnykID, 'to check no Overview.')
        else:
            print(content)
            print(SnykID, "to check, don't know whats this!")
            # print(html)


    return item_info

def collectSnykLanguageinfo():
    global Snyk_LanguageCVESnykItemID_map, Snyk_LanguageItemSID_list
    Snyk_LanguageCVESnykItemID_map = {}
    Snyk_LanguageItemSID_list = {}
    SnykItems = File_processing.walk_L1_FileNames( SnykItems_dir )
    # print(len(SnykItems))
    for SnyItem in SnykItems:
        if SnyItem.startswith('.'):
            print(SnyItem)
            continue

        full_path = SnykItems_dir + SnyItem
        # print(SnyItem)
        # print(full_path)
        SnyItemInfo = JSONFIle_processing.read(full_path)
        try:
            SnykID = SnyItemInfo['Snyk ID']
        except KeyError: # 说明该项为空
            print(SnyItem, 'To check, SnykID == Nono')
            continue

        # SnykID = SnyItemInfo['Snyk ID']
        language  = SnyItemInfo['Language']

        if 'CVE' in SnyItemInfo.keys():
            # CVEIDs = SnyItemInfo['CVE']
            # print(CVEIDs)
            # CVEIDs =[ 'CVE-'+ ele  for ele in SnyItemInfo['CVE'].split(SnyItemInfo['CVE'])[1:] ]
            # print(CVEIDs)
            CVEIDs= []
            for ele in SnyItemInfo['CVE'].split('CVE-'):
                if ele == '':
                    continue
                else:
                    CVEIDs.append('CVE-'+ele)
            # print(CVEIDs)
        else:
            CVEIDs = None


        if language in Snyk_LanguageItemSID_list.keys():
            Snyk_LanguageItemSID_list[language].append(SnykID)
        else:
            Snyk_LanguageItemSID_list[language] = [SnykID]

        if CVEIDs != None and len(CVEIDs)>0:
            for CVEID in CVEIDs:
                if language in Snyk_LanguageCVESnykItemID_map.keys():
                    if CVEID in Snyk_LanguageCVESnykItemID_map[language].keys():
                        Snyk_LanguageCVESnykItemID_map[language][CVEID].append(SnykID)
                    else:
                        Snyk_LanguageCVESnykItemID_map[language][CVEID] = [SnykID]
                else:
                    Snyk_LanguageCVESnykItemID_map[language] = {CVEID :[SnykID]}

    # 数据清理
    for language in Snyk_LanguageCVESnykItemID_map.keys():
        CVENumber =  len( Snyk_LanguageCVESnykItemID_map[language].keys())
        Snyk_LanguageCVESnykItemID_map[language]['CVENumber'] = CVENumber

        SIDNumber = 0
        for CVEitem in Snyk_LanguageCVESnykItemID_map[language].keys():
            if CVEitem == 'CVENumber':
                continue
            # print(Snyk_LanguageCVESnykItemID_map[language][CVEitem],language,CVEitem)
            Snyk_LanguageCVESnykItemID_map[language][CVEitem] = list( set( Snyk_LanguageCVESnykItemID_map[language][CVEitem] ) )
            SIDNumber += len(Snyk_LanguageCVESnykItemID_map[language][CVEitem])
            # if len(Snyk_LanguageCVESnykItemID_map[language][CVEitem])> 1:
            #     print(  Snyk_LanguageCVESnykItemID_map[language][CVEitem])
        Snyk_LanguageCVESnykItemID_map[language]['SIDNumber'] = SIDNumber

        print('Snyk_LanguageCVESnykItemID_map',language,CVENumber,SIDNumber)

    for language in Snyk_LanguageItemSID_list.keys():
        Snyk_LanguageItemSID_list[language] = list( set(Snyk_LanguageItemSID_list[language]) )
        SIDNumber =  len( Snyk_LanguageItemSID_list[language])
        # Snyk_LanguageItemSID_list[language]['SIDNumber'] = SIDNumber
        print('Snyk_LanguageItemSID_list',language,SIDNumber)


    # write
    JSONFIle_processing.write(json_content=Snyk_LanguageItemSID_list, path=Snyk_LanguageItemSID_list_path)
    JSONFIle_processing.write(json_content=Snyk_LanguageCVESnykItemID_map, path=Snyk_LanguageCVESnykItemID_map_path)



def extractSnykItemInfo(CVEID):
    global Snyk_LanguageItemSID_list, Snyk_LanguageCVESnykItemID_map
    SnykCVESID_map = Snyk_LanguageCVESnykItemID_map

    SnykItem = CVEItemInfo.CVEItem()

    for language in SnykCVESID_map.keys():
        try:
            if CVEID in SnykCVESID_map[language].keys():
                if language not in SnykItem.Language and SnykItem.Language == '':
                    SnykItem.Language = SnykItem.Language +  language
                else:
                    SnykItem.Language = SnykItem.Language + '__fdse__' + language

        except:
            continue
    # SnykItem.Language = SnykItem.Language.strip('__fdse__')

    # SnykItemSID = SnykCVESID_map[SnykItem.Language][CVEID][0]
    # print(SnykItemSID)
    # print(SnykItem.Language, CVEID)
    # if len( SnykCVESID_map[SnykItem.Language][CVEID] ) > 1:
    #     print("duplicate Snyk item:", CVEID, SnykCVESID_map[SnykItem.Language][CVEID])

    SnykItemSID_list = []
    for language in SnykItem.Language.split('__fdse__'):
        # print(SnykCVESID_map.keys())
        SnykItemSID_list.extend( SnykCVESID_map[language][CVEID] )
        print("duplicate Snyk item:", CVEID, SnykCVESID_map[language][CVEID])

    # CVE-2018-11251
    # for SnykItemSID in SnykCVESID_map[SnykItem.Language][CVEID]:
    for SnykItemSID in SnykItemSID_list:
        # print(SnykItemSID)
        Item_path = SnykItems_dir + SnykItemSID.replace(':','__') +'.json'
        SnykItem.ItemPath += SnykItems_dir + SnykItemSID.replace(':','__') +'.json' + '__fdse__'
        Item_data = JSONFIle_processing.read(Item_path)

        SnykItem.CVEID += CVEID +'__fdse__'
        SnykItem.Description += Item_data['overview'] +'__fdse__'

        if 'references' in Item_data.keys():
            if SnykItem.Reference == '':
                SnykItem.Reference = []
            for ele in Item_data['references']:
                if  len( ele.split('__fdse__') ) > 1:
                    SnykItem.Reference.append( ele.split('__fdse__')[1])
                else:
                    SnykItem.Reference.append(ele.split('__fdse__')[0])
        else:
            if SnykItem.Reference == '':
                SnykItem.Reference = None

        if SnykItem.Reference and len( SnykItem.Reference ) ==0:
            SnykItem.Reference  = None

        if SnykItem.Reference:
            SnykItem.Reference = sorted( list( set(  SnykItem.Reference )) )

        # SnykItem.CVSS2 = ''
        # SnykItem.CVSS3 = ''
        # SnykItem.CVSS2Vector = ''
        # SnykItem.CVSS3Vector = ''

        SnykItem.CVSS2 += str( Item_data['CVSS_Score'] )
        SnykItem.CVSS2Vector = Item_data['CVSS_Vector']

        SnykItem.CVSS3 = None
        SnykItem.CVSS3Vector = None


        # SnykItem.CWE = ''
        # SnykItem.AffectedVendorProductCPE = []
        # SnykItem.AffectedVendorProductVersionCPE = []


        VP_list = [ Item_data['Affected_product'] ]
        VP_list = [ urllib.parse.unquote(urllib.parse.unquote(ele)).lower().replace('.','_').replace('-','_').replace(':','__fdse__') for ele in VP_list ]
        patch_list = Item_data['Patch']
        if SnykItem.AffectedVendorProductCPE == '':
            SnykItem.AffectedVendorProductCPE = sorted(set(VP_list))
        elif SnykItem.AffectedVendorProductCPE:
            SnykItem.AffectedVendorProductCPE.extend(VP_list)
            SnykItem.AffectedVendorProductCPE = sorted(set(SnykItem.AffectedVendorProductCPE))


        if len( SnykItem.AffectedVendorProductCPE ) == 0:
            SnykItem.AffectedVendorProductCPE = None

        if SnykItem.Patch == '':
            SnykItem.Patch = sorted(set(patch_list))
        elif SnykItem.Patch:
            SnykItem.Patch.extend(patch_list)
            SnykItem.Patch = sorted(set(SnykItem.Patch))
        # print(SnykItem.Patch)

            
        # 数据清洗
        if SnykItem.Patch:
            patch_list_tem = []
            for ele in SnykItem.Patch:
                if len(  ele.split('github.com/') ) > 1:
                    # print(ele)
                    # print(SnykItem.Patch)
                    patch_list_tem.append(  'https://github.com/' +  ele.split('github.com/')[1])
            SnykItem.Patch = patch_list_tem
        if not SnykItem.Patch or len(SnykItem.Patch) == 0:
            SnykItem.Patch = None

    SnykItem.ItemPath = SnykItem.ItemPath.strip('__fdse__')
    SnykItem.CVEID = SnykItem.CVEID.strip('__fdse__')
    SnykItem.Description = SnykItem.Description.strip('__fdse__')
    return SnykItem



if __name__ == '__main__':
    # parseSnkyItemsPages()
    # collectSnykLanguageinfo()
    print(extractSnykItemInfo('CVE-2013-1856').Language)
    pass
