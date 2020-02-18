# -*- coding: utf-8 -*-

"""
Created on 2020-02-18 11:59  

@author: congyingxu
"""

import json

CVE_VPV_Data_path = "Local_Data/CVE_VulnerableVP.json"
CPE_VP_LocalRepo_path = "Local_Data/CPE_VP_LocalRepo.json"
LocalRepoVP_CVE_Data_path = "Local_Data/LocalRepoVP_CVE.json"

CVE_VPV_Data ={}
CPE_VP_LocalRepo_list ={}
LocalRepoVP_CVE_Data ={}

VP_count = 0
CVE_count = 0
def read():
    global CPE_VP_LocalRepo_list, CVE_VPV_Data
    with open(CPE_VP_LocalRepo_path,'r') as f:
        CPE_VP_LocalRepo_list =  list( json.loads( f.read() ).keys() )

    with open(CVE_VPV_Data_path,'r') as f:
        CVE_VPV_Data =  json.loads( f.read() )






def mapping():
    global CVE_count
    print( type(CVE_VPV_Data))
    for CVE in CVE_VPV_Data.keys():

        for VP in CVE_VPV_Data[CVE]:
            if VP in CPE_VP_LocalRepo_list:
                if VP in LocalRepoVP_CVE_Data.keys():
                    LocalRepoVP_CVE_Data[VP].append(CVE)
                else:
                    LocalRepoVP_CVE_Data[VP] = [CVE]

                CVE_count += 1


def write():

    with open(LocalRepoVP_CVE_Data_path,'w') as f:
        f.write( json.dumps( LocalRepoVP_CVE_Data,indent=4 ) )

if __name__ == '__main__':
    read()
    mapping()
    write()

    print(CVE_count)
    print(len( LocalRepoVP_CVE_Data.keys()) )