# -*- coding: utf-8 -*-

"""
Created on 2020-03-27 01:23  

@author: congyingxu
"""

import os
import random
import time

import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import UserAgents

def request_url(url):
    print('------------------------- url:' + url)
    headers = {'User-Agent': random.choice(UserAgents.agents)}
    url_content = requests.get(url, headers=headers, verify=False)
    # requests.
    return url_content


def session_get_url(url):
    # 参考博客 https://segmentfault.com/q/1010000008473868
    print('------------------------- url:' + url)
    session = requests.Session()
    session.headers = {
        'User-Agent': random.choice(UserAgents.agents),
        'Host': 'api.sourceclear.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cookie': 'sp_collector=430868eb-0555-41b2-b1a1-2f81d74b93f5',
        'Upgrade-Insecure-Requests': '1'
    }


    try :
        url_content = session.get(url,timeout=10)
    except:
        print("requests.exceptions.ReadTimeout")
        for i in range(130):
            print(i)
            time.sleep(1)
        print("requests.exceptions.ReadTimeout. sleep over")
        url_content = session.get(url, timeout=10)
    return url_content


def save_file_from_url(url, path):
    if os.path.exists(path):
        return
    time.sleep(random.randint(1, 3))
    headers = {'User-Agent': random.choice(UserAgents.agents)}
    package = requests.get(url, headers=headers)
    with open(path, "wb") as f:
        f.write(package.content)
    f.close()