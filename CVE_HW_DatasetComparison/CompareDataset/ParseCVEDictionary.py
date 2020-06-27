# -*- coding: utf-8 -*-

"""
Created on 2020-04-04 12:27  

@author: congyingxu

## 将CVE信息摘取独立出来
"""

from CommonFunction import JSONFIle_processing, File_processing
from bs4 import BeautifulSoup
from CVE_HW_DatasetComparison import CONFIG
import urllib

class CVEDictionary:

    def __init__(self):
        # self.CVE_dataset_file_path = "/Users/congyingxu/Downloads/CVE/DataSet-CVE_MITRE/allitems.xml"
        # self.CVEItems_dir = "/Users/congyingxu/Downloads/CVE/DataSet-CVE_MITRE/CVEItems/"
        self.CVE_dataset_file_path = CONFIG.CVE_dataset_file_path
        self.CVEItems_dir = CONFIG.CVEItems_dir

        self.CVE_dataset = '' # xml
        self.CVE_dataset_soup = ''
        self.CVE_Items = {}
        self.CVE_CVEID_list = []

        self.read()
        self.extractXML()


    def extractXML(self):
        print("Start to extractXML")
        ID_list = []
        xml = self.CVE_dataset
        # soup = BeautifulSoup(xml, 'html.parser')
        soup = BeautifulSoup(xml, 'lxml')
        self.CVE_dataset_soup = soup
        # item_list = soup.find_all('item', attrs={'type': 'CVE'})
        item_list = soup.find_all('item')
        for cve_item in item_list:
            cve_ID = cve_item["name"]
            ID_list.append(cve_ID)
            self.CVE_Items[cve_ID] = cve_item
            # print(cve_ID)
            # break
        self.CVE_CVEID_list = ID_list

    def read(self):
        print("Start to read")
        self.CVE_dataset = File_processing.read_TXTfile(self.CVE_dataset_file_path)

    def extractCVEitemInfo(self,CVEID):
        # CVE_Instance.extractCVEitemInfo("CVE-2018-0548")
        # {'CVE-2018-0548': {'data': {'Assigned': '20171127'}, 'desc': 'Cybozu Garoon 4.0.0 to 4.6.0 allows remote authenticated attackers to bypass access restriction to view the closed title of "Space" via unspecified vectors.', 'refs': ['https://support.cybozu.com/ja-jp/article/9886', 'http://jvn.jp/en/jp/JVN65268217/index.html']}}

        CVEID_Info = {}
        cve_item = self.CVE_Items[CVEID]
        phase = cve_item.find('phase')
        desc = cve_item.find('desc')
        refs_list = cve_item.find_all('ref')

        # description, reference, assign
        CVEID_Info[CVEID] = {}
        try:
            CVEID_Info[CVEID]['date'] = {phase.text : phase["date"]}
        except AttributeError:
            CVEID_Info[CVEID]['date'] = None
        CVEID_Info[CVEID]['desc'] = desc.text
        CVEID_Info[CVEID]['refs'] = []
        for ref in refs_list:
            src = ref["source"]
            try:
                url = ref["url"]
            except KeyError:
                continue
            full_url = src + "__fdse__" + url.replace('&amp;','&')
            full_url = urllib.parse.unquote(urllib.parse.unquote(full_url))
            CVEID_Info[CVEID]['refs'].append(full_url.replace('&amp;','&'))

        # CVEID_Info[CVEID]['refs'] = {phase.text: phase["date"]}

        # print(CVEID_Info)
        return CVEID_Info

    # 还不太好使
    def separateCVEItem(self):
        for key in self.CVE_Items.keys():
            print(key)
            path = self.CVEItems_dir + key +'.xml'

            f = open(path, "w")
            f.write(self.CVE_Items[key].encode(formatter='minimal'))
            f.close()
            # File_processing.write_TXTfile(  content= self.CVE_Items[key].encode(formatter='minimal') , path = )
            break


def testCVEItem():
    path = '/Users/congyingxu/Downloads/CVE/DataSet-CVE_MITRE/CVEItems/'
    xml = File_processing.read_TXTfile(path)
    # soup = BeautifulSoup(xml, 'html.parser')
    soup = BeautifulSoup(xml, 'lxml')
    soup.find()

if __name__ == '__main__':
    CVE_Instance = CVEDictionary()