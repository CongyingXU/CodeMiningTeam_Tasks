# -*- coding: utf-8 -*-

"""
Created on 2020-02-26 12:09  

@author: congyingxu

length D1_CVE_GA 1062
length D1_GA_CVE 7494

"""

from CommonFunction import JSONFIle_processing, File_processing

# read
GA_info_path = "Pre-Data/CVE_GAInfo.json"
GA_info = []

VulnerableVPv_CVE_path = "Pre-Data/VulnerableVP_CVE.json"
VulnerableVPv_CVE = []

CVE_VulnerableVPv_path = "Pre-Data/CVE_VulnerableVP.json"
CVE_VulnerableVPv = []


# write
VP_GAs_path = "Pre-Data/VP_GAs.json"
VP_GAs = {}

D1_GA_CVE_path = "Data/D1_GA_CVE.json"
D1_GAv_CVE_path = "Data/D1_GAv_CVE.json"
D1_CVE_GA_path = "Data/D1_CVE_GA.json"
D1_CVE_GAv_path = "Data/D1_CVE_GAv.json"

D1_GAv_CVE = {}
D1_GA_CVE = {}
D1_CVE_GA = {}
D1_CVE_GAv = {}




def read():
    global GA_info, VulnerableVPv_CVE, CVE_VulnerableVPv
    GA_info = JSONFIle_processing.read(GA_info_path)
    VulnerableVPv_CVE = JSONFIle_processing.read(VulnerableVPv_CVE_path)
    CVE_VulnerableVPv = JSONFIle_processing.read(CVE_VulnerableVPv_path)


def generateGA_CVEData():
    global D1_GA_CVE, VP_GAs, D1_GAv_CVE
    VP_NotVul = []
    for GA in GA_info.keys():
        VendorProduct = GA_info[GA]["VendorProduct"]
        if VendorProduct in VP_GAs.keys():
            VP_GAs[VendorProduct].append(GA)
        else:
            VP_GAs[VendorProduct] = [GA]

        if VendorProduct not in VulnerableVPv_CVE.keys():
            if VendorProduct not in VP_NotVul :
                # print( VendorProduct, "VendorProduct not in VulnerableVPv_CVE.keys()" )
                VP_NotVul.append(VendorProduct)
            continue

        D1_GA_CVE[GA] = []
        for version in VulnerableVPv_CVE[VendorProduct].keys():

            D1_GA_CVE[GA].extend( VulnerableVPv_CVE[VendorProduct][version] )


        # 清空为0的GA
        if len(D1_GA_CVE[GA]) == 0:
            D1_GA_CVE.pop(GA)
        else:
            D1_GA_CVE[GA] = list(set(D1_GA_CVE[GA]))
            D1_GAv_CVE[GA] = VulnerableVPv_CVE[VendorProduct]




def generateCVE_GAData():
    global D1_CVE_GA, D1_CVE_GAv
    for CVE in CVE_VulnerableVPv.keys():

        D1_CVE_GA[CVE] = []
        for VP in CVE_VulnerableVPv[CVE].keys():
            if VP in VP_GAs.keys():
                GAs = VP_GAs[VP]
                D1_CVE_GA[CVE].extend(GAs)
        # 清空为0的cve
        if len(D1_CVE_GA[CVE]) == 0:
            D1_CVE_GA.pop(CVE)
        else:
            D1_CVE_GA[CVE] = list( set( D1_CVE_GA[CVE] ) )


        D1_CVE_GAv[CVE] = {}
        for VP in CVE_VulnerableVPv[CVE].keys():
            if VP in VP_GAs.keys():
                GAs = VP_GAs[VP]
                for GA in GAs:
                    if GA in D1_CVE_GAv[CVE].keys():
                        print("AAAAAAAAlert! GA in D1_CVE_GAv[CVE_FSE].keys()")
                    else:
                        D1_CVE_GAv[CVE][GA] = CVE_VulnerableVPv[CVE][VP]
        # 清空为0的cve
        if len(D1_CVE_GAv[CVE]) == 0:
            D1_CVE_GAv.pop(CVE)






def write():
    global D1_CVE_GA, D1_GA_CVE, D1_CVE_GAv, VP_GAs, D1_GAv_CVE
    JSONFIle_processing.write(D1_CVE_GAv,D1_CVE_GAv_path)
    JSONFIle_processing.write(D1_CVE_GA,D1_CVE_GA_path)
    JSONFIle_processing.write(D1_GA_CVE,D1_GA_CVE_path)
    JSONFIle_processing.write(VP_GAs,VP_GAs_path)
    JSONFIle_processing.write(D1_GAv_CVE,D1_GAv_CVE_path)

    print("length D1_CVE_GA", len(D1_CVE_GA.keys()))
    print("length D1_GA_CVE", len(D1_GA_CVE.keys() ))


if __name__ == '__main__':
    read()
    generateGA_CVEData()
    generateCVE_GAData()
    write()