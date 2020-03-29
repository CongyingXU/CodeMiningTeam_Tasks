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