# -*- coding: utf-8 -*-

"""
Created on 2020-02-17 15:25  

@author: congyingxu

生成建库的 .sh脚本
"""

import json

VP_Git_Data = {}
VP_withGitPom_list = []
VP_with_LocalGitRepo_list = []


def readANDcollect():
    global VP_Git_Data
    with open("../Local_Data/VP_Git_POMFile.json",'r') as f:
        content = json.loads( f.read() )

    for VP in content.keys():
        if len(content[VP])>1:
            print(VP, content[VP])
        else:
            ele = content[VP]
            git_url_pom = list(ele.values())[0]
            git_url = "https://github.com/" + git_url_pom.split("/")[3] + '/' + git_url_pom.split("/")[4] + ".git"
            VP_Git_Data[VP] = git_url
            # print(VP_Git_Data)
            VP_with_LocalGitRepo_list.append(VP)






def generateBash():
    global VP_Git_Data

    content = ""
    for VP in VP_Git_Data:
        git_url = VP_Git_Data[VP]
        cmd_str = 'git clone ' + git_url + ' ' + VP + '\n'
        content += cmd_str

    f = open('../Local_Data/VP_clone.sh', 'w')
    f.write(content)

    with open("../Local_Data/CPE_VP_LocalRepo.json", 'w') as f:
        f.write(json.dumps(VP_Git_Data, indent=4))


readANDcollect()
generateBash()