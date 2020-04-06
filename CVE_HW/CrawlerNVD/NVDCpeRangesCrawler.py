# -*- coding: utf-8 -*-

"""
Created on 2020-04-05 11:09  

@author: congyingxu
"""

import sys
sys.path.append('../')  # 新加入的
sys.path.append('../../')  # 新加入的


import requests
import time
import random
import os
from CVE_HW.CrawlVearcode import UserAgents
from CommonFunction import JSONFIle_processing

from bs4 import BeautifulSoup
from CommonFunction import SeleniumCrawlerChrome
from fake_useragent import UserAgent




headers = {
 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
 'Accept-Encoding': 'gzip, deflate, sdch',
 'Accept-Language': 'zh-CN,zh;q=0.8',
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
}
cookies={'__jsluid':'8d3f4c75f437ca82cdfad85c0f4f7c25'}


root_url  = "https://nvd.nist.gov/vuln/detail/%s/cpes?expandCpeRanges=true"

# html_dir = "/home/hadoop/dfs/data/Workspace/CongyingXU/CVE/DataSet-NVD/NVDCpeRange/htmls/"
# NVD_CVEID_list_path = "/home/hadoop/dfs/data/Workspace/CongyingXU/CVE/MetaData/NVD_CVEID_list.json"

html_dir = "/Users/congyingxu/Downloads/CVE/DataSet-NVD/NVDCpeRange/htmls/"
items_dir = "/Users/congyingxu/Downloads/CVE/DataSet-NVD/NVDCpeRange/items/"
NVD_CVEID_list_path = "/Users/congyingxu/Downloads/CVE/MetaData/NVD_CVEID_list.json"


NVD_CVEID_list = JSONFIle_processing.read(NVD_CVEID_list_path)
NVD_CVEID_list = sorted( NVD_CVEID_list )




def session_get_url(url):
    # 参考博客 https://segmentfault.com/q/1010000008473868
    print('------------------------- url:' + url)
    session = requests.Session()
    session.headers = {
        'User-Agent': random.choice(UserAgents.agents),
        # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15',
        'Host': 'nvd.nist.gov',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cookie': '__utma=141729133.37727237.1585103462.1586073563.1586088246.13; __utmb=141729133.28.8.1586088475909; __utmc=141729133; __utmz=141729133.1586088246.13.3.utmcsr=baidu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt_GSA_CP1=1; __utmt_GSA_CP2=1; ASP.NET_SessionId=ipao5sdaehy5tpq3nqaembbo; CMSCsrfCookie=fii/dX5CmOBDsITOjyNB971VufofYmJK9Kru754X; CMSPreferredCulture=en-US; _ga=GA1.2.1592236263.1586088435; _gid=GA1.2.1961680022.1586088435',
        'Upgrade-Insecure-Requests': '1'
    }

    try :
        url_content = session.get(url)
    except:
        print("requests.exceptions.ReadTimeout")
        for i in range(10):
            print(i)
            time.sleep(1)
        print("requests.exceptions.ReadTimeout. sleep over")
        url_content = session.get(url)

    session.close()
    del(session)
    return url_content



def crawlerNVDCpeRanges(url, CVEID):
    # print('------------------------- url:' + url)
    # way 1
    html, title = SeleniumCrawlerChrome.getHtmlFromUrl(url)

    # # reponse = session_get_url(url)
    # # reponse = requests.get(url)
    # if reponse.status_code == 200:
    #     html = reponse.text.encode("utf-8", "ignore")
    # elif reponse.status_code == 408:
    #
    #     time.sleep(3)
    #     reponse = session_get_url(url)
    #     if reponse.status_code == 200:
    #         html = reponse.text.encode("utf-8", "ignore")
    #     else:
    #         print(reponse.status_code)
    #         print("Sth wrong with crawler!")
    #         html = 'Error'
    #
    # else:
    #     print(reponse.status_code)
    #     print("Sth wrong with crawler!")
    #     html = 'Error'

    return html


def wirtehtml(html,file_path):
    with open(file_path,'w') as f:
        f.write( str(html, encoding = "utf-8") )



def extractHtml(html):
    soup = BeautifulSoup(html, 'lxml')
    neighbor_div = soup.find(id="vulnCpeTreeLoading")
    parent_div = neighbor_div.parent
    input = parent_div.find('input')


def main():
    count  = 0
    for CVEID in NVD_CVEID_list[90000:]:
        count += 1
        full_url = root_url % CVEID
        file_path = html_dir + CVEID + '.html'
        if os.path.exists(file_path):
                continue

        print(CVEID,count)
        html = crawlerNVDCpeRanges(full_url, CVEID)
        if html == 'Error':
            break
        else:
            wirtehtml(html=html, file_path=file_path)

if __name__ == '__main__':
    main()