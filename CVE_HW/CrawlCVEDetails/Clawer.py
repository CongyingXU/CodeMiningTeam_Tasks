# -*- coding: utf-8 -*-

"""
Created on 2020-03-25 14:43  

@author: congyingxu
"""

DST_dir = ""
CVEList_path = ""

import requests

headers = {
 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
 'Accept-Encoding': 'gzip, deflate, sdch',
 'Accept-Language': 'zh-CN,zh;q=0.8',
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
}
cookies={'__jsluid':'8d3f4c75f437ca82cdfad85c0f4f7c25'}
url = 'https://www.cvedetails.com/cve/CVE-2017-12617'

reponse = requests.get(url,headers=headers,cookies=cookies)
print(reponse.text)

with open('test.html','w') as f:
    f.write(str(reponse.text))