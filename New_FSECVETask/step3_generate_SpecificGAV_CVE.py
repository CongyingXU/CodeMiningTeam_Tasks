# -*- coding: utf-8 -*-

"""
Created on 2020-02-26 14:36  

@author: congyingxu

摘除有具体的version 号的gav


length D3_SpecificGAv_CVE ga:  4390
length D3_NonSpecificGAv_CVE ga:  6498
length D3_WholeRangeGAv_CVE ga:  3061
length D3_PartRangeGAv_CVE ga:  5378
length D3_NoRangeGav_CVE ga:  1108

length D3_SpecificGAv_CVE gav:  108385
length D3_NonSpecificGAv_CVE gav:  32076
length D3_WholeRangeGAv_CVE gav:  12220
length D3_PartRangeGAv_CVE gav:  18748
length D3_NoRangeGav_CVE gav:  1108

length D3_SpecificGAv_CVE_cve :  275
length D3_NonSpecificGAv_CVE_cve :  850
length D3_WholeRangeGAv_CVE_cve :  120
length D3_PartRangeGAv_CVE_cve:  723
length D3_NoRangeGav_CVE_cve:  29
"""

from CommonFunction import JSONFIle_processing
from New_FSECVETask import step2_generate_smallsize_GA_CVE


D2_GAv_CVE = JSONFIle_processing.read(step2_generate_smallsize_GA_CVE.D2_GAv_CVE_path)

D3_SpecificGAv_CVE_path = "Data/D3_SpecificGAv_CVE.json"
D3_SpecificGAv_CVE = {}
D3_NonSpecificGAv_CVE_path = "Data/D3_NonSpecificGAv_CVE.json"
D3_NonSpecificGAv_CVE = {}

D3_WholeRangeGAv_CVE_path = "Data/D3_WholeRangeGAv_CVE.json"
D3_WholeRangeGAv_CVE = {}
D3_PartRangeGAv_CVE_path = "Data/D3_PartRangeGAv_CVE.json"
D3_PartRangeGAv_CVE = {}
D3_NoRangeGav_CVE_path = "Data/D3_NoRangeGav_CVE.json"
D3_NoRangeGav_CVE = {}


def read():
    pass

def generateSpecificGAV_CVE():

    global D3_SpecificGAv_CVE, D3_NonSpecificGAv_CVE, D3_WholeRangeGAv_CVE, D3_PartRangeGAv_CVE, D3_NoRangeGav_CVE

    vulne_GAV_count = 0
    for GA in D2_GAv_CVE.keys():
        for vulnerable_versionInfo in D2_GAv_CVE[GA].keys():
            vulne_GAV_count +=1
            version_info_list = vulnerable_versionInfo.split('||')
            Version_Num = version_info_list[0].split(':')[1]
            versionStartIncluding = version_info_list[1].split(':')[1]
            versionEndIncluding = version_info_list[2].split(':')[1]
            versionStartExcluding = version_info_list[3].split(':')[1]
            versionEndExcluding = version_info_list[4].split(':')[1]

            # 不存在这种情况
            if Version_Num !='NA' and( versionStartIncluding!='NA' or  versionEndIncluding!='NA' or  versionStartExcluding!='NA' or  versionEndExcluding!='NA'):
                print("LA JI!")
            if Version_Num != 'NA':
                GAV_str = GA + "__fdse__" + Version_Num
                # D3_SpecificGAv_CVE[GAV_str] = D2_GAv_CVE[GA][vulnerable_versionInfo]
                if GA in D3_SpecificGAv_CVE.keys():
                    if vulnerable_versionInfo in D3_SpecificGAv_CVE[GA].keys():
                        print("Bu Ying Daing!")
                    D3_SpecificGAv_CVE[GA][Version_Num] = D2_GAv_CVE[GA][vulnerable_versionInfo]
                else:
                    D3_SpecificGAv_CVE[GA] = {}
                    D3_SpecificGAv_CVE[GA][Version_Num] = D2_GAv_CVE[GA][vulnerable_versionInfo]
                # 避免最后一步
                continue

            # 两端都不为空
            elif (versionStartIncluding!='NA' or versionStartExcluding!='NA') and (versionEndIncluding!='NA' or versionEndExcluding!='NA'):
                if GA in D3_WholeRangeGAv_CVE.keys():
                    if vulnerable_versionInfo in D3_WholeRangeGAv_CVE[GA].keys():
                        print("Bu Ying Daing!")
                    D3_WholeRangeGAv_CVE[GA][vulnerable_versionInfo] = D2_GAv_CVE[GA][vulnerable_versionInfo]
                else:
                    D3_WholeRangeGAv_CVE[GA] = {}
                    D3_WholeRangeGAv_CVE[GA][vulnerable_versionInfo] = D2_GAv_CVE[GA][vulnerable_versionInfo]

            # 两端都为空
            elif (versionStartIncluding=='NA' and versionStartExcluding=='NA') and (versionEndIncluding=='NA' and versionEndExcluding=='NA'):
                if GA in D3_NoRangeGav_CVE.keys():
                    if vulnerable_versionInfo in D3_NoRangeGav_CVE[GA].keys():
                        print("Bu Ying Daing!")
                    D3_NoRangeGav_CVE[GA][vulnerable_versionInfo] = D2_GAv_CVE[GA][vulnerable_versionInfo]
                else:
                    D3_NoRangeGav_CVE[GA] = {}
                    D3_NoRangeGav_CVE[GA][vulnerable_versionInfo] = D2_GAv_CVE[GA][vulnerable_versionInfo]

            # 两端有一端不为空
            else:
                if GA in D3_PartRangeGAv_CVE.keys():
                    if vulnerable_versionInfo in D3_PartRangeGAv_CVE[GA].keys():
                        print("Bu Ying Daing!")
                    D3_PartRangeGAv_CVE[GA][vulnerable_versionInfo] = D2_GAv_CVE[GA][vulnerable_versionInfo]
                else:
                    D3_PartRangeGAv_CVE[GA] = {}
                    D3_PartRangeGAv_CVE[GA][vulnerable_versionInfo] = D2_GAv_CVE[GA][vulnerable_versionInfo]


            if GA in D3_NonSpecificGAv_CVE.keys():
                if vulnerable_versionInfo in D3_NonSpecificGAv_CVE[GA].keys():
                    print("Bu Ying Daing!")
                D3_NonSpecificGAv_CVE[GA][vulnerable_versionInfo] = D2_GAv_CVE[GA][vulnerable_versionInfo]
            else:
                D3_NonSpecificGAv_CVE[GA] = {}
                D3_NonSpecificGAv_CVE[GA][vulnerable_versionInfo] = D2_GAv_CVE[GA][vulnerable_versionInfo]

    print("vulne_GAV_count",vulne_GAV_count)


def write():
    global D3_SpecificGAv_CVE, D3_NonSpecificGAv_CVE, D3_WholeRangeGAv_CVE, D3_PartRangeGAv_CVE, D3_NoRangeGav_CVE

    JSONFIle_processing.write(D3_SpecificGAv_CVE,D3_SpecificGAv_CVE_path)
    JSONFIle_processing.write(D3_NonSpecificGAv_CVE, D3_NonSpecificGAv_CVE_path)
    JSONFIle_processing.write(D3_WholeRangeGAv_CVE, D3_WholeRangeGAv_CVE_path)
    JSONFIle_processing.write(D3_PartRangeGAv_CVE, D3_PartRangeGAv_CVE_path)
    JSONFIle_processing.write(D3_NoRangeGav_CVE,D3_NoRangeGav_CVE_path)

    print("length D3_SpecificGAv_CVE ga: ",len(D3_SpecificGAv_CVE.keys()))
    print("length D3_NonSpecificGAv_CVE ga: ", len(D3_NonSpecificGAv_CVE.keys()))
    print("length D3_WholeRangeGAv_CVE ga: ", len(D3_WholeRangeGAv_CVE.keys()))
    print("length D3_PartRangeGAv_CVE ga: ", len(D3_PartRangeGAv_CVE.keys()))
    print("length D3_NoRangeGav_CVE ga: ", len(D3_NoRangeGav_CVE.keys()))

    len_D3_SpecificGAv_CVE = 0
    D3_SpecificGAv_CVE_cve = set()
    for GA in D3_SpecificGAv_CVE.keys():
        len_D3_SpecificGAv_CVE += len(D3_SpecificGAv_CVE[GA].keys())
        for v in D3_SpecificGAv_CVE[GA].keys( ):
            D3_SpecificGAv_CVE_cve.update(D3_SpecificGAv_CVE[GA][v])

    len_D3_NonSpecificGAv_CVE = 0
    D3_NonSpecificGAv_CVE_cve = set()
    for GA in D3_NonSpecificGAv_CVE.keys():
        len_D3_NonSpecificGAv_CVE += len(D3_NonSpecificGAv_CVE[GA].keys())
        for v in D3_NonSpecificGAv_CVE[GA].keys():
            D3_NonSpecificGAv_CVE_cve.update( D3_NonSpecificGAv_CVE[GA][v])

    len_D3_WholeRangeGAv_CVE = 0
    D3_WholeRangeGAv_CVE_cve = set()
    for GA in D3_WholeRangeGAv_CVE.keys():
        len_D3_WholeRangeGAv_CVE += len(D3_WholeRangeGAv_CVE[GA].keys())
        for v in D3_WholeRangeGAv_CVE[GA].keys( ):
            D3_WholeRangeGAv_CVE_cve.update(D3_WholeRangeGAv_CVE[GA][v])

    len_D3_PartRangeGAv_CVE = 0
    D3_PartRangeGAv_CVE_cve = set()
    for GA in D3_PartRangeGAv_CVE.keys():
        len_D3_PartRangeGAv_CVE += len(D3_PartRangeGAv_CVE[GA].keys())
        for v in D3_PartRangeGAv_CVE[GA].keys( ):
            D3_PartRangeGAv_CVE_cve.update(D3_PartRangeGAv_CVE[GA][v])

    len_D3_NoRangeGav_CVE = 0
    D3_NoRangeGav_CVE_cve = set()
    for GA in D3_NoRangeGav_CVE.keys():
        len_D3_NoRangeGav_CVE += len(D3_NoRangeGav_CVE[GA].keys())
        for v in D3_NoRangeGav_CVE[GA].keys( ):
            D3_NoRangeGav_CVE_cve.update(D3_NoRangeGav_CVE[GA][v])

    print("length D3_SpecificGAv_CVE gav: ",len_D3_SpecificGAv_CVE)
    print("length D3_NonSpecificGAv_CVE gav: ", len_D3_NonSpecificGAv_CVE)
    print("length D3_WholeRangeGAv_CVE gav: ", len_D3_WholeRangeGAv_CVE)
    print("length D3_PartRangeGAv_CVE gav: ", len_D3_PartRangeGAv_CVE)
    print("length D3_NoRangeGav_CVE gav: ", len_D3_NoRangeGav_CVE)

    print("length D3_SpecificGAv_CVE_cve : ", len(D3_SpecificGAv_CVE_cve))
    print("length D3_NonSpecificGAv_CVE_cve : ", len(D3_NonSpecificGAv_CVE_cve))
    print("length D3_WholeRangeGAv_CVE_cve : ", len(D3_WholeRangeGAv_CVE_cve))
    print("length D3_PartRangeGAv_CVE_cve: ", len(D3_PartRangeGAv_CVE_cve))
    print("length D3_NoRangeGav_CVE_cve: ", len(D3_NoRangeGav_CVE_cve))



if __name__ == '__main__':
    read()
    generateSpecificGAV_CVE()
    write()



