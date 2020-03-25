# -*- coding: utf-8 -*-

"""
Created on 2020-02-15 23:27  

@author: congyingxu
"""

import sys
sys.path.append('../')  # 新加入的

from CVE_FSE import mappingVPGitRepo
import requests
from bs4 import BeautifulSoup
import json
import os


VP_GIT_REPO_DATA = mappingVPGitRepo.VPGitMap().VP_GIT_REPO_DATA

pomfile_count = 0
VP_GIT_POM_DATA = {}
VP_GIT_POM_DATA_file  = "Local_Data/VP_Git_POMFile.json"


def getPOMfile(soup,git_url,VP):
        global pomfile_count
        print(git_url)

        table_list = soup.find_all('table', attrs={'class': 'files js-navigation-container js-active-navigation-container'})
        if len( table_list) >0:
            table = table_list[0]
            # print(table)
            tr_list = table.find_all('tr', attrs={'class': 'js-navigation-item'})
            # print(tr_list)
            for tr in tr_list:
                td = tr.find('td', attrs={'class': 'content'})
                a = tr.find('a')
                try:
                    title = a["title"]
                    if title == "Go to parent directory":
                        continue
                except:
                    pass
                if a == None:
                    print("None A!'")
                    continue
                part_url = a["href"]
                # print(part_url)
                file_name =  part_url.split("/")[-1]
                # print(file_name)

                if file_name.find('.') > -1: # 文件
                    if file_name.lower() == "pom.xml":
                        sub_git_url = "https://github.com" + part_url
                        sub_response = requests.get(sub_git_url)
                        print(sub_response.status_code)
                        sub_html = sub_response.text


                        pom_filee_name = str(pomfile_count) + "__fdse__" + VP.replace('/','-') + ".html"
                        with open("POM_htmlfiles/" + pom_filee_name , 'w') as f:
                            f.write( sub_html )


                        pomfile_count += 1
                        if VP in VP_GIT_POM_DATA.keys():
                            VP_GIT_POM_DATA[VP].update( { pom_filee_name:sub_git_url } )
                            # print(VP_GIT_POM_DATA)
                        else:
                            VP_GIT_POM_DATA[VP] = {pom_filee_name,sub_git_url}

                    else:
                        pass
                else: # 文件夹
                    pass
                    # sub_git_url = "https://github.com" + part_url
                    # sub_response = requests.get(sub_git_url)
                    # sub_html = sub_response.text
                    # sub_soup = BeautifulSoup(sub_html, 'html.parser')
                    # # print(sub_response.text)
                    # print(sub_response.status_code)
                    #
                    # getPOMfile(sub_soup, sub_git_url,VP)

            # lastUpdated = soup.find_all('lastUpdated', limit=1)[0]
            # lastUpdated_time = lastUpdated.get_text()

def getGitHtml():
    global VP_GIT_POM_DATA

    for VP in list(VP_GIT_REPO_DATA.keys())[2600:]:
        print(VP)

        if os.path.exists(VP_GIT_POM_DATA_file):
            with open(VP_GIT_POM_DATA_file,'r') as f:
                VP_GIT_POM_DATA = json.loads( f.read() )

        # print(VP_GIT_POM_DATA)
        if VP in VP_GIT_POM_DATA.keys():
            continue
        else:
            VP_GIT_POM_DATA[VP] = {}

        for git_url in VP_GIT_REPO_DATA[VP]:

            response = requests.get(git_url)
            html = response.text
            print("response",response.status_code)
            soup = BeautifulSoup(html, 'html.parser')

            getPOMfile(soup,git_url,VP)


        # if VP not in VP_GIT_POM_DATA.keys():
        #     VP_GIT_POM_DATA[VP] = {}
        write()






def write():
    # print(VP_GIT_POM_DATA)
    with open(VP_GIT_POM_DATA_file,"w") as f:
        f.write(  json.dumps(VP_GIT_POM_DATA,indent =4 ) )


getGitHtml()

