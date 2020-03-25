# -*- coding: utf-8 -*-

"""
Created on 2020-03-25 18:04  

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

url = "https://snyk.io/vuln/%s"

root_dir = "/Users/congyingxu/Downloads/"
# root_dir = "/Volumes/My Passport/"


page_store_dir = root_dir + "CVE/CrawledSnykHtmls/MavenItemPages/"
snyk_maven_item_list_path = root_dir + "CVE/CrawledSnykHtmls/SnykMavenItemLists.json"
Snyk_dtem_data_path = root_dir + "CVE/CrawledSnykHtmls/SnykMavenItemInfo.json"
Snyk_vuln_lib_data_path = root_dir + "CVE/CrawledSnykHtmls/Snyk_vuln_lib.json"

Snyk_dtem_data = {}
Snyk_vuln_lib_data = {}

def getItempage(url):
    print("getPage", url)

    reponse = requests.get(url, headers=headers, cookies=cookies)
    # print( reponse.status_code )
    if reponse.status_code == 200:
        html = reponse.text
    else:
        print("Sth wrong with crawler!")
        html = 'Error'


    return html


def extractItemInfo(html):
    global Snyk_vuln_lib_data

    ItemInfo = {"CVEs":[] , "GithubCommit":[] }
    vuln_lib = {}

    soup = BeautifulSoup(html, 'html.parser')

    # Artifact version
    strong = soup.find_all('strong')
    if len(strong) != 3:
        print( len( strong),'should be 3' )
    # print(strong)
    Artifact = strong[0].text.strip('\n').strip('          ')
    Artifact = Artifact.replace(':',"__fdse__")
    Version = strong[1].text.strip('\n').strip('          ')
    ItemInfo["Artifact"] = Artifact
    ItemInfo["Version"] = Version

    # CVE
    div = soup.find_all('div',attrs={'class':'vuln-sidebar-offset'})[0]
    div = div.find_all('div', attrs={'class': 'card__content'})[-1]
    dl = div.find_all('dl')[-1]
    a = dl.find_all('a')
    for a_item in a:
        a_url = a_item['href']
        if 'CVE' in a_url.upper():
            CVE_name = a_url.split("name=")[-1]
            ItemInfo["CVEs"].append(CVE_name)


    # print( len( soup.find_all('div',attrs={"class":"card card--markdown"}) ))
    div = soup.find_all('div',attrs={"class":"card card--markdown"})[0]
    # print( len( div.find_all('ul' ) ))
    ul = div.find_all('ul' )[-1]
    # for ul in  div.find_all('ul'):
    for li in ul.find_all('li'):
            # print(li.text)
            if 'GitHub Commit' in li.text:
                a = li.find_all('a')[0]
                # print(a["href"])
                ItemInfo["GithubCommit"].append(a["href"])

    if len(ItemInfo["GithubCommit"])==0 or len(ItemInfo["CVEs"]) ==0:
        print( ItemInfo )

    # write Snyk_vuln_lib_data
    if len(ItemInfo["CVEs"]) !=0:
        for cve in ItemInfo["CVEs"]:
            vuln_lib[Artifact] = {cve:ItemInfo["GithubCommit"]}

        if Artifact in Snyk_vuln_lib_data.keys():
            Snyk_vuln_lib_data[Artifact].update({cve:ItemInfo["GithubCommit"]})
            if cve in Snyk_vuln_lib_data[Artifact].keys():
                print(Snyk_vuln_lib_data[Artifact][cve])
                print(ItemInfo["GithubCommit"])
        else:
            Snyk_vuln_lib_data[Artifact] = vuln_lib[Artifact]

    return  ItemInfo


def readSnykitemList():
    snyk_maven_item_list = JSONFIle_processing.read(snyk_maven_item_list_path)
    return snyk_maven_item_list

def wirtehtml(html,file_name):
    with open(page_store_dir + file_name +'.html','w') as f:
        f.write( str(html) )



def main():
    global Snyk_dtem_data,Snyk_vuln_lib_data
    snyk_maven_item_list = readSnykitemList()
    Snyk_dtem_data  =JSONFIle_processing.read(Snyk_dtem_data_path)
    Snyk_vuln_lib_data = JSONFIle_processing.read(Snyk_vuln_lib_data_path)

    for Snykitem in snyk_maven_item_list:
        if Snykitem in Snyk_dtem_data.keys():
            continue

        # url = 'https://snyk.io/vuln/SNYK-JAVA-ORGWEBJARS-480332'
        # html = getItempage(url)
        html = getItempage( url % Snykitem )
        if html == 'Error':
            break

        wirtehtml(html,Snykitem)
        ItemInfo = extractItemInfo(html)
        Snyk_dtem_data[Snykitem] = ItemInfo


        # break

        JSONFIle_processing.write(Snyk_dtem_data,Snyk_dtem_data_path)
        JSONFIle_processing.write(Snyk_vuln_lib_data,Snyk_vuln_lib_data_path)

if __name__ == '__main__':
    main()