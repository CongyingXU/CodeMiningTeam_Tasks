# -*- coding: utf-8 -*-

"""
Created on 2020-02-06 17:41  

@author: congyingxu

used to map VP to Git repo url
"""

from CVE_FSE import processingCPEDictionary
import json


VP_GitRepo_Map_file_path = "Local_Data/VPGitRepoMap.json"


class VPGitMap:

    CPE_REFERENCE_DATA = {}
    VP_GIT_REPO_DATA = {}
    VP_GITREPO_MAP_FILE_PATH = VP_GitRepo_Map_file_path

    def __init__(self):
        self.read_VP_GIT_REPO_DATA()

    def read_VP_GIT_REPO_DATA(self):
        with open(self.VP_GITREPO_MAP_FILE_PATH) as f:
            self.VP_GIT_REPO_DATA = json.loads( f.read() )


    def read(self):
        self.CPE_REFERENCE_DATA = processingCPEDictionary.ProcessCPEDictionnary().read_reference_data()

    def process(self):
        # get all data
        for VP_ele in self.CPE_REFERENCE_DATA["VP_references"].keys():
            for reference_type_ele in self.CPE_REFERENCE_DATA["VP_references"][VP_ele].keys():
                for url in self.CPE_REFERENCE_DATA["VP_references"][VP_ele][reference_type_ele]:
                    if "github.com" in url:
                        url  = url.strip("/")

                        if len( url.split("/") ) > 4:
                            processed_url = "https://github.com/" + url.split("/")[3] + '/' + url.split("/")[4]
                            if VP_ele in self.VP_GIT_REPO_DATA.keys():
                                if processed_url not in self.VP_GIT_REPO_DATA[VP_ele]:
                                    self.VP_GIT_REPO_DATA[VP_ele].append( processed_url )
                            else:
                                self.VP_GIT_REPO_DATA[VP_ele] = [processed_url]

        # # processing all data
        # for VP in self.VP_GIT_REPO_DATA.keys():
        #     git_repo = set()
        #     for git_url in self.VP_GIT_REPO_DATA[VP]:





    def write(self):
        with open(self.VP_GITREPO_MAP_FILE_PATH,'w') as f:
            f.write( json.dumps(self.VP_GIT_REPO_DATA, indent = 4) )


    def main(self):
        self.read()
        self.process()
        self.write()

if __name__ == '__main__':
    VPGitMap().main()