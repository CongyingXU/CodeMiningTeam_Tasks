# -*- coding: utf-8 -*-

"""
Created on 2020-01-06 15:36  

@author: congyingxu
统计800个项目中的所有dependency GAV
"""

from CommonFunction import File_processing,JSONFIle_processing

class collectDependency:

    pojlist = []
    DG_data = {}

    def __init__(self, data_path, json_path):
        self.data_path = data_path
        self.json_path = json_path


    def get_pojlist(self):
        self.pojlist = File_processing.walk_FileDir(self.data_path)
        print(self.pojlist)


    def collect_dependecy(self):

        for poj in self.pojlist:
            print(poj)
            if poj.endswith(".DS_Store"):
                continue
            poj_DGinfo = JSONFIle_processing.read(poj)
            for item in poj_DGinfo:
                groupId = item['groupId']
                artifactId = item['artifactId']
                if 'version' in item.keys():
                    version = item['version']
                else:
                    version  = 'unavailable'

                GA = groupId + '__fdse__' + artifactId

                if GA in self.DG_data.keys():
                    if version in self.DG_data[GA]:
                        pass
                    else:
                        self.DG_data[GA].append(version)
                else:
                    self.DG_data[GA] = [version]
            print(self.DG_data)

    def write(self):
        JSONFIle_processing.write(self.DG_data ,self.json_path)

    def main(self):
        self.get_pojlist()
        self.collect_dependecy()
        self.write()
        print('xxxxx')


if __name__ == '__main__':
    DG_Data_path = 'poj_DG_data/data/dependency/raw'
    result_json_path = 'dependency.json'
    collectDependency(DG_Data_path,result_json_path).main()