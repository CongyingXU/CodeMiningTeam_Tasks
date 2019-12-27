#!/usr/bin/env python
# encoding: utf-8
"""

Created on 2019/12/27 10:46
@Author : CongyingXu

利用LibEffort-Jar，跑出pojs中的dependency
生成对应的batch
"""

import json


poj_list = []
cmd_list = []
def read_pojs():
    global poj_list
    with open('projects.json','r') as f:
        poj_list = json.loads(f.read())


def generate_batch_files():
    f = open('generateDG.sh','a')

    out_path = '/home/hadoop/dfs/data/ThirdPartyLibs/Source/projects_DG/poj_DG_data/'
    config_path = '/home/hadoop/dfs/data/ThirdPartyLibs/Source/projects_DG/path_config.properties'
    poj_path = ''


    for poj in poj_list:
        poj_path = 'projects_git/'+poj +'/'
        cmd_str = 'java -jar /home/hadoop/dfs/data/ThirdPartyLibs/Source/projects_DG/LibEffort-jar-with-dependencies.jar ' + poj_path +' '+ config_path +' ' + out_path + '\n'
        f.write(cmd_str)




if __name__ == '__main__':
    read_pojs()
    generate_batch_files()