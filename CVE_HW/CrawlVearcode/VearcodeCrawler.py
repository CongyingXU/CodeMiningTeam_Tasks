# -*- coding: utf-8 -*-

"""
Created on 2020-03-27 01:21  

@author: congyingxu
"""

import sys
sys.path.append('../')  # 新加入的

import json
import os

import requests

from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import CrawlUtil
import FileUtil


class SeleniumCrawler:

    def __init__(self):
        # self.driver_path = r'C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe'
        self.driver_path =  '/Users/congyingxu/Documents/chromedriver'

    def crawl(self):
        # 初始化一个driver，并且指定chromedriver的路径
        self.browser = webdriver.Chrome(executable_path=self.driver_path)

        # elements = self.browser.find_elements_by_css_selector("[class=\"grid pt--\"]")
        total_num = 0

        language  = "all" # python javascript
        # self.browser.get('https://sca.analysiscenter.veracode.com/vulnerability-database/search#query=type:vulnerability%20language:' + language)
        self.browser.get('https://sca.analysiscenter.veracode.com/vulnerability-database/search#query=type:vulnerability')
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

    def request_detail_json(self):
        detail_dir = "../datas/vulnerability/detail/"
        components_url = "https://api.sourceclear.com/artifacts/components/"

        files = os.listdir(detail_dir)
        for file in files:
            if file.endswith(".html"):
                sid = file[:-5].replace("sid-", "")
                output_file = detail_dir + "affected_lib/" + sid + ".json"
                if os.path.exists(output_file):
                    continue
                response = CrawlUtil.request_url(components_url + sid)
                if response.status_code == requests.codes.ok:
                    # print(response.text)
                    FileUtil.write_json(output_file, json.loads(response.text))
                else:
                    print("sssssssid " + sid)

    def crawl_safe_version(self):
        lib_vulne = FileUtil.read_json("../datas/vulnerability/detail/lib_vulne.json")
        print(len(lib_vulne))

        count = 0
        for lib in lib_vulne:
            count += len(lib_vulne[lib])
        print(count)


if __name__ == "__main__":
    sc = SeleniumCrawler()
    sc.crawl()
    sc.crawl_detail()
    sc.request_detail_json()
    # sc.crawl_safe_version()