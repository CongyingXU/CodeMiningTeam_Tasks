# -*- coding: utf-8 -*-

"""
Created on 2020-03-25 16:51  

@author: congyingxu
"""

import requests
from bs4 import BeautifulSoup
from CommonFunction import JSONFIle_processing


headers = {
 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
 'Accept-Encoding': 'gzip, deflate, sdch',
 'Accept-Language': 'zh-CN,zh;q=0.8',
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
}
cookies={'__jsluid':'8d3f4c75f437ca82cdfad85c0f4f7c25'}

url = "https://snyk.io/vuln/page/%s?type=maven"
page_store_dir = "/Volumes/My Passport/CVE/CrawledSnykHtmls/MavenListPages/"
snyk_maven_item_list_path = "/Volumes/My Passport/CVE/CrawledSnykHtmls/SnykMavenItemLists.json"


snyk_maven_item_list = []


def getPage(url):
    print( "getPage",url )

    reponse = requests.get(url, headers=headers, cookies=cookies)

    # print( reponse.status_code )
    if reponse.status_code == 200:
        pass
    else:
        print( "Sth wrong with crawler!" )

    html = reponse.text
    return html


def extractSnykIDs(html):
    global snyk_maven_item_list

    soup = BeautifulSoup(html, 'html.parser')
    tbody = soup.find_all('tbody')
    # print( len( tbody) )


    for tr in tbody[0].find_all('tr'):
        a = tr.find_all('a')
        # print( len(a),a[0] )
        SnykID = a[0]['href'].split('/')[-1]
        snyk_maven_item_list.add(SnykID)

    print("len snyk_maven_item_list", len(snyk_maven_item_list))



def wirtehtml(html,file_name):
    with open(page_store_dir + file_name +'page.html','w') as f:
        f.write( str(html) )

def writeitem_list():
    JSONFIle_processing.write( list(snyk_maven_item_list) , snyk_maven_item_list_path)

def main():
    global snyk_maven_item_list
    snyk_maven_item_list = set(JSONFIle_processing.read(snyk_maven_item_list_path))


    for pageindex in range(1,117):
        html = getPage( url % pageindex )
        wirtehtml(html,str(pageindex))
        extractSnykIDs(html)
        writeitem_list()
        # break


if __name__ == '__main__':
    main()