# -*- coding: utf-8 -*-

"""
Created on 2020-01-14 14:18  

@author: congyingxu

生成 Geelu的项目list
"""

import os
import json

rootdir = '/Users/congyingxu/Downloads/CodeMiningTeam_Tasks/GenerateDG/poj_DG_data/data/'

# rootdir -> list: all Folders in Level 1
def walk_L1_Folders():
    global rootdir
    for parent, dirnames, filenames in os.walk(rootdir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        return dirnames


def main():
    poj_list = walk_L1_Folders()
    print(poj_list)
    with open("poj_list.json",'w') as f:
        f.write( json.dumps( poj_list,indent=4 ) )

if __name__ == '__main__':
    main()

