# -*- coding: utf-8 -*-

"""
Created on 2020-03-25 14:43  

@author: congyingxu
"""

import sys
sys.path.append('../')  # 新加入的
sys.path.append('../../')  # 新加入的

DST_dir = ""
CVEList_path = ""

import time
import random
import requests
from bs4 import BeautifulSoup
from CommonFunction import JSONFIle_processing
from fake_useragent import UserAgent
# import selenium
# from CommonFunction import SeleniumCrawlerFirefox

headers = {
 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
 'Accept-Encoding': 'gzip, deflate, sdch',
 'Accept-Language': 'zh-CN,zh;q=0.8',
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
}
cookies={'__jsluid':'8d3f4c75f437ca82cdfad85c0f4f7c25'}



url = 'https://www.cvedetails.com/cve/%s'
# root_dir = "/Users/congyingxu/Downloads/"
# root_dir = "/Volumes/My Passport/"
root_dir = "/home/hadoop/dfs/data/Workspace/CongyingXU/"


page_store_dir = root_dir + "CVE/CrawledCVEdetailsHtmls/Pages/"
CVE_CVEID_list_path = root_dir + 'CVE/MetaData/CVE_CVEID_list.json'
CVEDetails_CVEID_list_path = root_dir + 'CVE/CrawledCVEdetailsHtmls/CVEDetails_CVEID_list.json'

CVE_CVEID_list = JSONFIle_processing.read(CVE_CVEID_list_path)
CVEDetails_CVEID_list = []



def getCVEdetailsItem(url):
    print("getPage", url)
    # way 1
    # reponse = requests.get(url, headers={
    #     "User-Agent": str(UserAgent(path='/Users/congyingxu/Documents/fake_useragent_0.1.11.json').random)},
    #                        cookies=cookies)
    reponse = requests.get(url)

    print(reponse.status_code)
    if reponse.status_code == 200:
        html = reponse.text.encode("utf-8", "ignore")
        title = 'NULL'
    else:
        html = 'Error'
        title = 'www.cvedetails.com'

    # way 2
    # html,title  = SeleniumCrawlerFirefox.getHtmlFromUrl(url)

    return html,title

def writePage(html,filename):

    with open(page_store_dir + filename + 'atCVEDetails.html', 'w') as f:
        f.write(str(html, encoding = "utf-8")  )




def main():
    global CVEDetails_CVEID_list
    CVEDetails_CVEID_list = JSONFIle_processing.read(CVEDetails_CVEID_list_path)


    for cve in CVE_CVEID_list:
        # time.sleep(random.random() * 5)
        if cve in CVEDetails_CVEID_list:
            continue

        #获取html
        html,title = getCVEdetailsItem( url % cve)
        if html=='Error':
            break

        #log标记
        CVEDetails_CVEID_list.append(cve)  # 用于log
        # 随机写入，防丢失
        if int(cve[-1]) == 0:
            print("write")
            JSONFIle_processing.write(CVEDetails_CVEID_list, CVEDetails_CVEID_list_path)

        # 保存html
        # 该cveid不存在
        if title == 'CVE security vulnerability database. Security vulnerabilities, exploits, references and more':
            continue
        elif title == 'www.cvedetails.com': #访问不成功
            break
        else:
            writePage(html, cve)

        # break

    JSONFIle_processing.write(CVEDetails_CVEID_list,CVEDetails_CVEID_list_path)



if __name__ == '__main__':
    main()

