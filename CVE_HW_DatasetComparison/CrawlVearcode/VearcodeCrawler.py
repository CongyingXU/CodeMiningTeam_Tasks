# -*- coding: utf-8 -*-

"""
Created on 2020-03-27 01:21  

@author: congyingxu


swift 2
os 2800
csharp 360
php 1100
go 540
objectivec 720
ruby 680
cpp 640
python 920
javascript 1880
java 1700
总数和：11342
并集数据量：11221



len(sid_list) 11221
------------------------- url:https://api.sourceclear.com/artifacts/components/6799
401
sssssssid sid-6799
------------------------- url:https://api.sourceclear.com/artifacts/components/20709
401
sssssssid sid-20709
------------------------- url:https://api.sourceclear.com/artifacts/components/1796
401
sssssssid sid-1796
------------------------- url:https://api.sourceclear.com/artifacts/components/12316
401
sssssssid sid-12316
------------------------- url:https://api.sourceclear.com/artifacts/components/7540
401
sssssssid sid-7540
------------------------- url:https://api.sourceclear.com/artifacts/components/5638
401
sssssssid sid-5638
------------------------- url:https://api.sourceclear.com/artifacts/components/16661
401
sssssssid sid-16661
------------------------- url:https://api.sourceclear.com/artifacts/components/13708
401
sssssssid sid-13708
------------------------- url:https://api.sourceclear.com/artifacts/components/7294
401
sssssssid sid-7294
------------------------- url:https://api.sourceclear.com/artifacts/components/5446
401
sssssssid sid-5446
------------------------- url:https://api.sourceclear.com/artifacts/components/7334
401
sssssssid sid-7334
------------------------- url:https://api.sourceclear.com/artifacts/components/5505
401
sssssssid sid-5505
------------------------- url:https://api.sourceclear.com/artifacts/components/13251
401
sssssssid sid-13251
failure_count 13
"""

import sys
sys.path.append('../')  # 新加入的
sys.path.append('../../')  # 新加入的
from CommonFunction import JSONFIle_processing



import json
import os
import random
import requests

from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from CVE_HW_DatasetComparison import CONFIG

import CrawlUtil
import FileUtil
import UserAgents

class SeleniumCrawler:

    def __init__(self):
        # self.driver_path = r'C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe'
        self.driver_path =  CONFIG.ChromeDriver_path
        self.CrawledVearCodeHtmls_dir = CONFIG.VearCodeCrawledVearCodeHtmls_dir
        self.LanguageVulnerList_dir = CONFIG.VearCodeLanguageVulnerList_dir
        self.VearCodeItems_dir = CONFIG.VearCodeItems_dir
        self.VearCodeArtifact_dir = CONFIG.VearCodeArtifact_dir
        # language = "os"  # csharp php go swift objectivec ruby cpp python javascript java
        self.language_list = ['swift', 'os', 'csharp', 'php', 'go', 'objectivec', 'ruby', 'cpp', 'python', 'javascript',
                         'java']

    def crawl(self):
        # 初始化一个driver，并且指定chromedriver的路径
        self.browser = webdriver.Chrome(executable_path=self.driver_path)

        # elements = self.browser.find_elements_by_css_selector("[class=\"grid pt--\"]")
        total_num = 0

        #       
        language  = "os"  # csharp php go swift objectivec ruby cpp python javascript
        self.browser.get('https://sca.analysiscenter.veracode.com/vulnerability-database/search#query=type:vulnerability%20language:' + language)
        # self.browser.get('https://sca.analysiscenter.veracode.com/vulnerability-database/search#query=type:vulnerability')
        elements = self.browser.find_elements_by_css_selector(".grid.pt--")
        curr_num = len(elements)
        # print(curr_num)
        while curr_num <= total_num:
            time.sleep(3)
            elements = self.browser.find_elements_by_css_selector(".grid.pt--")
            curr_num = len(elements)
        else:
            total_num =curr_num
            print(total_num)

        while True:
            self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            elements = self.browser.find_elements_by_css_selector(".grid.pt--")
            curr_num = len(elements)
            while curr_num <= total_num:
                time.sleep(3)
                elements = self.browser.find_elements_by_css_selector(".grid.pt--")
                curr_num = len(elements)
            else:
                total_num = curr_num
                print(total_num)
                FileUtil.write_file("../datas/vulnerability/" + str(total_num) + language + ".html", self.browser.page_source)

        # wait = WebDriverWait(self.browser, 30)
        # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "flex--footer")))

        # print("正在获取网页数据...")
        # soup = BeautifulSoup(self.browser.page_source, "lxml")
        # print(self.browser.page_source)
        # self.browser.close()

    def crawl_detail(self):
        # self.browser = webdriver.Chrome(executable_path=self.driver_path)

        lines = FileUtil.read_file_lines("../datas/vulnerability/detail/error.txt")
        no_lib = FileUtil.read_json("../datas/vulnerability/no_lib.json")
        output_dir = "../datas/vulnerability/detail/"

        input_file = "../datas/vulnerability/1660.html"
        java_vuls = FileUtil.read_file_string(input_file)
        soup = BeautifulSoup(java_vuls, "lxml")
        elements = soup.find_all(class_='grid pt--')
        print(len(elements))
        names = set()
        for e in elements:
            link_element = e.find(class_='link--no-underline')
            url = link_element["href"]
            name = url.replace("/summary", "")
            name = name[name.rfind("/") + 1:]
            # if os.path.exists(output_dir + str(name) + ".html"):
            #     continue
            if name not in no_lib:
                continue
            # print(name)
            names.add(name)
            if name not in lines:
                print(name)
        print(len(names))
            # try:
            #     self.browser.get("https://sca.analysiscenter.veracode.com" + url)
            #     wait = WebDriverWait(self.browser, 30)
            #     wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".font-family--code")))
            #     FileUtil.write_file(output_dir + str(name) + ".html", self.browser.page_source)
            # except:
            #     FileUtil.append_file(output_dir + "error.txt", name)
            #     FileUtil.write_file(output_dir + str(name) + ".html", self.browser.page_source)

        # input_file = "../datas/vulnerability/detail/error.txt"
        # java_vuls = FileUtil.read_file_lines(input_file)
        # total = 0
        # for url in java_vuls:
        #     if url == "":
        #         continue
        #     total += 1
        #     name = url.replace("/summary", "")
        #     name = name[name.rfind("/") + 1:]
        #     if name in no_lib:
        #         FileUtil.append_file(output_dir + "new_error.txt", name)
        #         continue
        #     os.remove(output_dir + str(name) + ".html")
        #     print(name)
        # print(total)

    def extract_sid_list(self):


        # 读取语言漏洞的列表信息，提取sid
        sid_list = []
        sid_url_list = []
        for language in self.language_list:
            input_file = self.LanguageVulnerList_dir + language + '.html'
            java_vuls = FileUtil.read_file_string(input_file)
            soup = BeautifulSoup(java_vuls, "lxml")
            elements = soup.find_all(class_='grid pt--')
            print(language, len(elements))
            pre_part_sid_url = "https://sca.analysiscenter.veracode.com"
            for e in elements:
                link_element = e.find(class_='link--no-underline')
                url = pre_part_sid_url + link_element["href"]
                sid_url_list.append(url)

                sid = url.split('/')[-2]
                sid_list.append(sid)
                # name = url.replace("/summary", "")
                # name = name[name.rfind("/") + 1:]
            # break
        print(len(sid_list), len(sid_url_list))
        sid_list = list(set(sid_list))
        sid_url_list = list(set(sid_url_list))
        print(len(sid_list), len(sid_url_list))
        JSONFIle_processing.write(sid_list, self.CrawledVearCodeHtmls_dir + 'vearcode_sid_list.json')
        JSONFIle_processing.write(sid_url_list, self.CrawledVearCodeHtmls_dir + 'veracode_sid_url_list.json')


    def request_detail_json(self):

        #根据sid list，请求相关的json数据
        sid_list = JSONFIle_processing.read(self.CrawledVearCodeHtmls_dir + 'vearcode_sid_list.json')
        print("len(sid_list)",len(sid_list))
        sid_list  =list( set( sid_list ) )
        print("len(sid_list)", len(sid_list))
        components_url = "https://api.sourceclear.com/artifacts/components/"
        failure_count = 0

        for sid in sid_list:

                output_file = self.VearCodeItems_dir + sid + ".json"
                if os.path.exists(output_file):
                    continue
                # 参考博客 https://segmentfault.com/q/1010000008473868
                url = components_url + sid[4:]
                response = CrawlUtil.session_get_url(url)
                # print(response.status_code)
                # print( response.text)
                if response.status_code == requests.codes.ok:
                    # print(response.text)
                    FileUtil.write_json(output_file, json.loads(response.text))
                else:
                    failure_count +=1
                    print( response.status_code )
                    # print(response.text)
                    print("sssssssid " + sid)
        print("failure_count",failure_count)

    def request_Artifact_json(self,start_index):

        # 根据sid list，请求相关的json数据
        components_url = "https://api.sourceclear.com/catalog/components/"

        Vearcode_404List_path = 'Vearcode_404List.json'
        Vearcode_404List = JSONFIle_processing.read(Vearcode_404List_path)

        for sid in range(start_index,10000 * 100):

            output_file = self.VearCodeArtifact_dir + str(sid) + ".json"
            if os.path.exists(output_file) or sid in Vearcode_404List:
                continue
            # 参考博客 https://segmentfault.com/q/1010000008473868
            url = components_url + str(sid)
            response = CrawlUtil.session_get_url(url)
            # print(response.status_code)
            # print( response.text)
            if response.status_code == requests.codes.ok:
                # print(response.text)
                FileUtil.write_json(output_file, json.loads(response.text))
            else:
                print(response.status_code)
                # print(response.text)
                print("sssssssid " + str(sid))
                if str( response.status_code ) == '404':
                    print('write')
                    Vearcode_404List = JSONFIle_processing.read(Vearcode_404List_path) # 因为多进程并发，所以保证写之前，读取更新一下！
                    Vearcode_404List.append(sid)
                    JSONFIle_processing.write(Vearcode_404List,Vearcode_404List_path)



if __name__ == "__main__":
    sc = SeleniumCrawler()
    # sc.crawl() # 对应语言，根据链接，浏览器爬取list信息
    # sc.extract_sid_list() # 抽取list信息
    # sc.request_detail_json() # 爬取对应sid的信息
    sc.request_Artifact_json( int(sys.argv[1]) ) # 爬取artifact的信息