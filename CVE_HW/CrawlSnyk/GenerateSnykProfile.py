# -*- coding: utf-8 -*-

"""
Created on 2020-04-02 09:09  

@author: congyingxu

用于h汇总Snky相关数据：
-SID Number
-Language Number & SID Number
-Meta-Module


。。。。
-CVE Number


Sid_Num 10334
JAVA 3502
DOTNET 673
npm 1184
JS 959
COCOAPODS 744
PYTHON 1036
RUBY 683
PHP 1348
GOLANG 205

"""

from CVE_HW.CrawlSnyk import SnykItemCrawler,MavenCrawler
from CommonFunction import File_processing,JSONFIle_processing

from bs4 import BeautifulSoup


Profile_path = MavenCrawler.root_dir + "CVE/CrawledSnykHtmls/SnykDataSetProfile.json"

Profile = {}
sid_list = []
Language_data = {}

def CollectFromList():
    global Profile
    # Coleect -SID Number
    SnykItem_dir = SnykItemCrawler.page_store_dir
    Sid_Num = len( File_processing.walk_L1_FileNames(SnykItem_dir) )
    Profile['SnykItemNumber'] = Sid_Num


    # Coleect -Language Number & SID Number
    SnykList_dir = MavenCrawler.page_store_dir
    filenames = File_processing.walk_L1_FileNames(SnykList_dir)
    print('len(filenames)',len(filenames))
    for filename in filenames:
        file_path = SnykList_dir + filename
        extractHtmlFile(file_path)

    print('Sid_Num',Sid_Num)
    print('Sid_Num', len(sid_list))
    for type in Language_data.keys():
        print(type, len(Language_data[type]) )




def extractHtmlFile(file_path):
    global Language_data,sid_list
    with open(file_path,'r') as f:
        file_content = f.read()

    soup = BeautifulSoup(file_content, 'html.parser')
    tbody = soup.find('tbody')
    tr_list = tbody.find_all('tr')

    for tr in tr_list:
        # ID
        span = tr.find('span',attrs = {'class':'l-push-left--sm'})
        href = span.a["href"]
        Sid = href.split('/')[-1]

        # type
        td = tr.find_all('td', attrs = {'class':'t--sm'})[1]
        type = td.text.strip('\n').strip(' ').strip('\n')

        # print(Sid,type)

        if type in Language_data.keys():
            Language_data[type].append( Sid )
        else:
            Language_data[type] = [Sid]
        sid_list.append(Sid)


def CollectFromItem():
    # Coleect -SID Number
    SnykItem_dir = SnykItemCrawler.page_store_dir
    Sid_Num = len(File_processing.walk_L1_FileNames(SnykItem_dir))


    # Coleect -Language Number & SID Number
    item_list_path = MavenCrawler.snyk_maven_item_list_path
    item_list = JSONFIle_processing.read(item_list_path)

    for item in item_list:
        if ':' in item:
            type = item.split(":")[0]
        elif '-' in item :
            type = item.split('-')[1]
        else:
            print(item)


        sid_list.append(item)
        if type in Language_data.keys():
            Language_data[type].append(item)
        else:
            Language_data[type] = [item]

    print('Sid_Num', Sid_Num)
    print('Sid_Num', len(sid_list))
    for type in Language_data.keys():
        print(type, len(Language_data[type]))




    # write
    Profile['SnykItemNumber'] = len(sid_list)
    # Meta-Mudule
    Profile['Meta-Module'] = [
        'Title',
        'Affected Package and vesion',
        'Overview',
        'Details',
        'Types of attacks',
        'Affected environments',
        'How to prevent',
        'Remediation',
        'Reference (Github Commit)',
        'CVSS Score and Vector',
        'Credit',
        'CVE',
        'CWE',
        'SNYK-ID',
        'Disclosed Date',
        'Published Data'
    ]
    Profile['SnykTypeItems'] = []
    for type in Language_data.keys():

        Profile['SnykTypeItems'].append({type: len(Language_data[type]) })
        # Profile['SnykTypes'][-1]['Numbers'] = len(Language_data[type])
        Profile['SnykTypeItems'][-1]['IDs'] = Language_data[type]


    JSONFIle_processing.write(Profile,Profile_path)



if __name__ == '__main__':
    CollectFromItem()
