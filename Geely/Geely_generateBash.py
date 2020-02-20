# -*- coding: utf-8 -*-

"""
Created on 2020-01-14 14:23  

@author: congyingxu
"""
import os
import json



start  = 0
end = 2

poj_list = []



def read_pojs():
    global poj_list
    with open("poj_list.json",'r') as f:
        poj_list = json.loads(f.read())


def generate_batch_files():
    f = open('Geely_generateDG.sh','a')

    out_path = '/geely/fdse/output/'
    config_path = '/geely/fdse/LibDetectRec/LibDetectJava/config/path_config.properties'



    for poj in poj_list[start:end]:
        poj_path = '/home/jenkins/workspace/'+poj +'/'
        cmd_str = '/geely/tools/jdk1.8.0_181/bin/java -jar /geely/fdse/LibHarmo-jar-with-dependencies.jar ' + out_path +' '+ config_path +' ' + poj_path + '\n'
        f.write(cmd_str)
    f.close()
    print('ok!')





def main():
    read_pojs()
    generate_batch_files()

if __name__ == '__main__':
    main()