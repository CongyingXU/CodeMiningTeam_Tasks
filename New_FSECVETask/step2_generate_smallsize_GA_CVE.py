# -*- coding: utf-8 -*-

"""
Created on 2020-02-26 13:18  

@author: congyingxu
通过 GAV-CVE-buggymethod + used_vulne_libs_wangying,数据删掉共有

vp count:  335
cve count:  1014
length D2_GA_CVE 7265

公共 = 7494 - 7265
"""
from CommonFunction import JSONFIle_processing, File_processing
from New_FSECVETask import step1_generate_GA_CVE

# D1_GA_CVE = step1_generate_GA_CVE.D1_GA_CVE

D1_GA_CVE = JSONFIle_processing.read(step1_generate_GA_CVE.D1_GA_CVE_path)
D1_GAv_CVE = JSONFIle_processing.read(step1_generate_GA_CVE.D1_GAv_CVE_path)
GA_info = JSONFIle_processing.read(step1_generate_GA_CVE.GA_info_path)

D2_GA_CVE_path = "Data/D2_GA_CVE.json"
D2_GA_CVE = {}

D2_GAv_CVE_path = "Data/D2_GAv_CVE.json"
D2_GAv_CVE = {}

GAV_CVE_BuggyMethod_path = "Pre-Data/GAV_CVE_BuggyMethod.json"
GAV_CVE_BuggyMethod = {}

used_vulne_libs_wangying_path = "Pre-Data/used_vulne_libs_wangying.json"
used_vulne_libs_wangying = {}

lib_vulne_path = "Pre-Data/lib_vulne.json"
lib_vulne = {}


def init():
    global GAV_CVE_BuggyMethod,D2_GA_CVE
    GAV_CVE_BuggyMethod = JSONFIle_processing.read(GAV_CVE_BuggyMethod_path)

    if File_processing.pathExist(D2_GA_CVE_path):
        D2_GA_CVE = JSONFIle_processing.read(D2_GA_CVE_path)

def read():
    global GAV_CVE_BuggyMethod, D2_GA_CVE, used_vulne_libs_wangying, lib_vulne
    GAV_CVE_BuggyMethod = JSONFIle_processing.read(GAV_CVE_BuggyMethod_path)
    used_vulne_libs_wangying = JSONFIle_processing.read(used_vulne_libs_wangying_path)
    lib_vulne = JSONFIle_processing.read(lib_vulne_path)


def generate_smallsize_GA_CVE():
    global D2_GA_CVE, D2_GAv_CVE, D1_GAv_CVE, lib_vulne
    # generate wangying collect GA
    wangying_collect_GA  = []
    for GAV in GAV_CVE_BuggyMethod:
        GA = GAV.split("__fdse__")[0] + "__fdse__" + GAV.split("__fdse__")[1]
        wangying_collect_GA.append(GA)

    wangying_collect_GA.extend( list(used_vulne_libs_wangying.keys()) + list(lib_vulne.keys()) )
    wangying_collect_GA = list( set(wangying_collect_GA) )

    # generate_smallsize_GA_CVE
    for GA in D1_GA_CVE.keys():
        if GA in wangying_collect_GA:
            continue
        else:
            D2_GA_CVE[GA] = D1_GA_CVE[GA]

    # generate_smallsize_GA_CVE
    for GA in D1_GA_CVE.keys():
        if GA in wangying_collect_GA:
            continue
        else:
            D2_GAv_CVE[GA] = D1_GAv_CVE[GA]




def write():
    global D2_GA_CVE, GA_info
    JSONFIle_processing.write(D2_GA_CVE,D2_GA_CVE_path)
    JSONFIle_processing.write(D2_GAv_CVE, D2_GAv_CVE_path)

    vp_set = []
    cve_set = []
    for GA in D2_GA_CVE.keys():
        cve_set.extend( D2_GA_CVE[GA] )
        vp_set.append(GA_info[GA]["VendorProduct"])

    vp_set = set( vp_set )
    cve_set = set(cve_set)

    print("length D2_GA_CVE", len(D2_GA_CVE.keys()))
    print("cve count: ",len( cve_set ))
    print("vp count: ", len(vp_set))


# init()

if __name__ == '__main__':
    read()
    generate_smallsize_GA_CVE()
    write()


