#!/usr/bin/env python
# encoding: utf-8
"""

Created on 2019/12/27 10:46
@Author : CongyingXu

利用LibEffort-Jar，跑出pojs中的dependency
生成对应的batch
"""

import json
from CommonFunction import File_processing
from CommonFunction import JSONFIle_processing


poj_list = []
cmd_list = []
def read_pojs():
    global poj_list
    with open('projects.json','r') as f:
        poj_list = json.loads(f.read())


def generate_batch_files():
    f = open('generateDG.sh','a')

    out_path = 'poj_DG_data0216'
    config_path = 'path_config.properties'
    poj_path = ''


    for poj in poj_list:
        poj_path = '../projects_2_5/'+poj +''
        cmd_str = 'java -jar LibEffort-jar-with-dependencies.jar ' + out_path +' '+ config_path +' ' + poj_path + '\n'
        f.write(cmd_str)
    print('mm')


def check_pojname():
    ServerPojList = File_processing.read_TXTfile('ServerPojList.txt').replace('\n',' ').split(' ')
    ServerPojList = [ ele.strip('\n') for ele in ServerPojList if ele != '']

    print(ServerPojList)


    poj_list =  JSONFIle_processing.read('projects.json')
    print(poj_list)
    count = 0

    for ele in poj_list:
        if ele in ServerPojList:
            print(ele)
            count +=1

    print('count ',count)

# check_pojname()



if __name__ == '__main__':
    read_pojs()
    generate_batch_files()



