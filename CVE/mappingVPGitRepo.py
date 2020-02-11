# -*- coding: utf-8 -*-

"""
Created on 2020-02-06 17:41  

@author: congyingxu

used to map VP to Git repo url
"""

from CVE import processingCPEDictionary
import json


VP_GitRepo_Map_file_path = "Local_Data/VPGitRepoMap.json"


class VPGitMap:

    CPE_REFERENCE_DATA = {}
    VP_GIT_REPO_DATA = {}
    VP_GITREPO_MAP_FILE_PATH = VP_GitRepo_Map_file_path

    def read(self):
        self.CPE_REFERENCE_DATA = processingCPEDictionary.ProcessCPEDictionnary().read_reference_data()

    def process(self):
        for VP_ele in self.CPE_REFERENCE_DATA["VP_references"].keys():
            for reference_type_ele in self.CPE_REFERENCE_DATA["VP_references"][VP_ele].keys():
                for url in self.CPE_REFERENCE_DATA["VP_references"][VP_ele][reference_type_ele]:
                    if "github.com" in url:
                        if VP_ele in self.VP_GIT_REPO_DATA.keys():

                            self.VP_GIT_REPO_DATA[VP_ele].append( url )
                        else:
                            self.VP_GIT_REPO_DATA[VP_ele] = [url]

    def write(self):
        with open(self.VP_GITREPO_MAP_FILE_PATH,'w') as f:
            f.write( json.dumps(self.VP_GIT_REPO_DATA, indent = 4) )


    def main(self):
        self.read()
        self.process()
        self.write()

if __name__ == '__main__':
    VPGitMap().main()