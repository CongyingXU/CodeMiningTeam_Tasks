# -*- coding: utf-8 -*-

"""
Created on 2020-04-18 10:22  

@author: congyingxu
"""

from CommonFunction import JSONFIle_processing

from CVE_HW_DatasetComparison.AnalyseComparedData import DifferenceAnalysisItemTemplate
from CVE_HW_DatasetComparison import CONFIG

from CVE_HW_DatasetComparison.CrawlerNVD import ParseNVD


NVDvsCVEdetails_DifferentAnalysis_path = CONFIG.NVDvsCVEdetails_DifferentAnalysis_path
NVDvsCVEdetailsDifferentData_path = CONFIG.NVDvsCVEdetails_Different_path
NVDvsCVEdetails_AnalysisData =   DifferenceAnalysisItemTemplate.DifferenceAnalysis(NVDvsCVEdetailsDifferentData_path)

DifferenDataInfo = NVDvsCVEdetails_AnalysisData.DifferenDataInfo


def setMetadata():
    global DifferenDataInfo, NVDvsCVEdetails_AnalysisData

    # meta-data
    # self.ComparedPart1_name = ''
    # self.ComparedPart2_name = ''
    # self.ComparedPart1_CVENum = ''
    # self.ComparedPart2_CVENum = ''
    NVDvsCVEdetails_AnalysisData.ComparedPart1_name = 'NVD'
    NVDvsCVEdetails_AnalysisData.ComparedPart2_name = 'CVEdetails'
    NVDvsCVEdetails_AnalysisData.ComparedPart1_CVENum = '139742'
    NVDvsCVEdetails_AnalysisData.ComparedPart2_CVENum = '123454'

    # # 对比的CVE总量及不同量
    # self.ComparedCVE_TotalNum = ''
    # self.ComparedCVE_DiffNum = ''
    NVDvsCVEdetails_AnalysisData.ComparedCVE_TotalNum = len( DifferenDataInfo['ComparedCVEIDs'] )
    NVDvsCVEdetails_AnalysisData.ComparedCVE_DiffNum = len(DifferenDataInfo.keys()) - 4  # 减去vector相关的那个, 72093

    # # 对比的Vector，及每个ele对应的C格式
    # self.ComparedVector = ''  # 存储 vector 和 case
    # self.ComparedVector_CaseDifferentNums = ''  # 存储数量
    # self.ComparedVector_CaseDifferentCVEs = ''  # 春初具体CVEID
    NVDvsCVEdetails_AnalysisData.ComparedVector = ['1 desc', '2 refs','3 CVSS', '4 CWE','5 AffectedVP', '6 AffectedVPV', '7 OvalDefinition']
    NVDvsCVEdetails_AnalysisData.ComparedCase = ['2-1: Reject in CVE','2-2: same url set but with duplicate urls',
                                                 '2-3: CVEdetails lack ref', '2-4: NVD lack ref', '2-5: other',
                                                 '5-1: Different VP set', '5-2: NVD is the subset', '5-3: CVEdetails is the subset',
                                                 '6-1: Upto CVEdetails Maximum 700 VPV', '6-2: Cperange', '6-3: AND-OR', '6-4: Other']
    NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentCVEs = {'1': [],
                                                                     '2':[], '2-1':[], '2-2':[], '2-3':[], '2-4':[], '2-5':[],
                                                                     '3': [],
                                                                     '4': [],
                                                                     '5': [],'5-1':[], '5-2':[], '5-3':[],
                                                                     '6': [],'6-1':[], '6-2':[], '6-3':[], '6-4':[],
                                                                     '7': []}
    NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentNums = {'1': 0,
                                                                     '2': 0, '2-1':0, '2-2':0, '2-3':0, '2-4':0, '2-5':0,
                                                                     '3': 0,
                                                                     '4': 0,
                                                                     '5': 0,'5-1':0, '5-2':0, '5-3':0,
                                                                     '6': 0,'6-1':0, '6-2':0, '6-3':0, '6-4':0,
                                                                     '7': 0}


    # self.NotComparedCVE_TotalNumandPartName = ''
    # self.NotComparedCase = ''
    # self.NotCompared_CaseNums = ''  # 存储数量
    # self.NotCompared_CaseCVEs = ''  # 春初具体CVEID
    NVDvsCVEdetails_AnalysisData.NotComparedCVE_TotalNum = 'NVD:' + str(len(DifferenDataInfo['NotInNVDCVEIDs'])) + '  CVEdetails:' + str(len(DifferenDataInfo['NotInCVEdetailsCVEIDs']))
    NVDvsCVEdetails_AnalysisData.NotComparedCase = [
        '#-1: Not in CVEdetails and not in NVD',
        '#-2: Not in CVEdetails but in NVD',
        '#-3: In CVEdetails but not in NVD']
    NVDvsCVEdetails_AnalysisData.NotCompared_CaseNums = {'#-1': 0, '#-2': 0, '#-3': 0}  # 存储数量
    NVDvsCVEdetails_AnalysisData.NotCompared_CaseCVEs = {'#-1': [], '#-2': [], '#-3': []}  # 春初具体CVEID


def analyseData():
    global DifferenDataInfo, NVDvsCVEdetails_AnalysisData

    # analyse CVE not in NVD / CVEdetails
    NotInNVD_set  = set( DifferenDataInfo['NotInNVDCVEIDs'] )
    NotInCVEdetails_set = set( DifferenDataInfo['NotInCVEdetailsCVEIDs'] )
    # 全集
    NotInUnion_list = list( NotInNVD_set.union(NotInCVEdetails_set))
    NVDvsCVEdetails_AnalysisData.NotCompared_CaseNums['#-1'] = len( NotInUnion_list )
    NVDvsCVEdetails_AnalysisData.NotCompared_CaseCVEs['#-1'] = NotInUnion_list
    # CVEdetails 补集
    NotInCVEdetailsDifference_list = list( NotInCVEdetails_set.difference(NotInNVD_set)  )
    NVDvsCVEdetails_AnalysisData.NotCompared_CaseNums['#-2'] = len(NotInCVEdetailsDifference_list)
    NVDvsCVEdetails_AnalysisData.NotCompared_CaseCVEs['#-2'] = NotInCVEdetailsDifference_list
    # NVD 补集
    NotInNVDDifference_list = list(NotInNVD_set.difference(NotInCVEdetails_set))
    NVDvsCVEdetails_AnalysisData.NotCompared_CaseNums['#-3'] = len(NotInNVDDifference_list)
    NVDvsCVEdetails_AnalysisData.NotCompared_CaseCVEs['#-3'] = NotInNVDDifference_list

    # analyse compared CVE Items
    for CVEID in DifferenDataInfo.keys():
        if not CVEID.startswith('CVE-'):
            continue
        # print(CVEID)
        # CVEID = 'CVE-2011-4905'
        CVE_differentInfo = DifferenDataInfo[CVEID]
        flag = str(CVE_differentInfo['flag'])
        if flag in NVDvsCVEdetails_AnalysisData.ComparedVector_FlagNums.keys():
            NVDvsCVEdetails_AnalysisData.ComparedVector_FlagNums[flag] += 1
            NVDvsCVEdetails_AnalysisData.ComparedVector_FlagCVEs[flag].append(CVEID)
        else:
            NVDvsCVEdetails_AnalysisData.ComparedVector_FlagNums[flag] = 1
            NVDvsCVEdetails_AnalysisData.ComparedVector_FlagCVEs[flag] = [CVEID]

        if '1' in flag:
            NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentNums['1'] += 1
            NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentCVEs['1'].append(CVEID)
            pass

        if '2' in flag:
            NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentNums['2'] += 1
            NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentCVEs['2'].append(CVEID)

            CVEdetailsurl_list = CVE_differentInfo['CVEdetails']['Reference']
            NVDurl_list = CVE_differentInfo['NVD']['Reference']
            # 2-1 Reject
            if '** REJECT **' in CVE_differentInfo['NVD']['Description']:
                NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentNums['2-1'] += 1
                NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentCVEs['2-1'].append(CVEID)
            # 2-2 same url set but with duplicate urls
            elif case2_2(CVEdetailsurl_list, NVDurl_list):
                NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentNums['2-2'] += 1
                NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentCVEs['2-2'].append(CVEID)
            # 2-3 CVE缺失
            elif case2_3(CVEdetailsurl_list, NVDurl_list):
                NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentNums['2-3'] += 1
                NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentCVEs['2-3'].append(CVEID)
            # 2-4 NVD缺失
            elif case2_4(CVEdetailsurl_list, NVDurl_list):
                NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentNums['2-4'] += 1
                NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentCVEs['2-4'].append(CVEID)
            # 2-5 other:
            else:
                NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentNums['2-5'] += 1
                NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentCVEs['2-5'].append(CVEID)

        if '3' in flag:
            NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentNums['3'] += 1
            NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentCVEs['3'].append(CVEID)

        if '4' in flag:
            NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentNums['4'] += 1
            NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentCVEs['4'].append(CVEID)

        if '5' in flag:
            NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentNums['5'] += 1
            NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentCVEs['5'].append(CVEID)

            CVEdetailsVP_list = CVE_differentInfo['CVEdetails']['AffectedVendorProductCPE']
            NVDVP_list = CVE_differentInfo['NVD']['AffectedVendorProductCPE']
            # 2-1
            # 2-2 same url set but with duplicate urls
            if case5_1(CVEdetailsVP_list, NVDVP_list):
                NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentNums['5-1'] += 1
                NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentCVEs['5-1'].append(CVEID)
            # 2-3 CVE缺失
            elif case5_2(CVEdetailsVP_list, NVDVP_list):
                NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentNums['5-2'] += 1
                NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentCVEs['5-2'].append(CVEID)
            # 2-4 NVD缺失
            elif case5_3(CVEdetailsVP_list, NVDVP_list):
                NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentNums['5-3'] += 1
                NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentCVEs['5-3'].append(CVEID)
            # 2-5 other:
            else:
                NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentNums['5-4'] += 1
                NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentCVEs['5-4'].append(CVEID)

        if '6' in flag:
            NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentNums['6'] += 1
            NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentCVEs['6'].append(CVEID)

            CVEdetailsVPV_list = CVE_differentInfo['CVEdetails']['AffectedVendorProductVersionCPE']
            NVDVPV_list = CVE_differentInfo['NVD']['AffectedVendorProductVersionCPE']

            NVDItemInfo = ParseNVD.extractNVDItemInfo(CVEID)
            # * 6-1: upto CVEdetails Maximum 700
            # * 6-2: range affected CPE version // 处理粗糙
            # * 6-3: AND-OR // 处理粗糙
            # * 6-4: Other
            if case6_1(CVEdetailsVPV_list, NVDVPV_list):
                NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentNums['6-1'] += 1
                NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentCVEs['6-1'].append(CVEID)
            elif NVDItemInfo.tag_CpeRange == True:
                NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentNums['6-2'] += 1
                NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentCVEs['6-2'].append(CVEID)
            elif NVDItemInfo.tag_ANDOR == True:
                NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentNums['6-3'] += 1
                NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentCVEs['6-3'].append(CVEID)
            else:
                NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentNums['6-4'] += 1
                NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentCVEs['6-4'].append(CVEID)

        if '7' in flag:
            NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentNums['7'] += 1
            NVDvsCVEdetails_AnalysisData.ComparedVector_CaseDifferentCVEs['7'].append(CVEID)




def case2_2(CVEurl_list, NVDurl_list):
    if CVEurl_list and NVDurl_list: # 都不为None
       if sorted( set(CVEurl_list) ) == sorted( set(NVDurl_list) ):
           return True
       else:
           return False
    elif not CVEurl_list and not NVDurl_list: # 都为None
        return True
    else: # other
        return False

def case2_3(CVEurl_list, NVDurl_list):
    if not NVDurl_list:
        return False
    elif not CVEurl_list:
        return True
    else:
        CVEurl_list = sorted(set(CVEurl_list))
        NVDurl_list = sorted(set(NVDurl_list))
        for url in CVEurl_list:
            if url in NVDurl_list:
                continue
            else:
                return False
        return True

def case2_4(CVEurl_list, NVDurl_list):
    if not CVEurl_list:
        return False
    elif not NVDurl_list:
        return True
    else:
        CVEurl_list = sorted(set(CVEurl_list))
        NVDurl_list = sorted(set(NVDurl_list))
        for url in NVDurl_list:
            if url in CVEurl_list:
                continue
            else:
                return False
        return True


# different set
def case5_1(CVEurl_list, Snykurl_list):
    if CVEurl_list and Snykurl_list: # 都不为None
       if sorted( set(CVEurl_list) ) == sorted( set(Snykurl_list) ): # 相等
           return False
       elif set(CVEurl_list).issubset(set(Snykurl_list)) or set(Snykurl_list).issubset(set(CVEurl_list)): # 子集关系
           return False
       else:
           return True
    elif not CVEurl_list and not Snykurl_list: # 都为None
        return False
    else: # 肯定是子集关系了
        return False


# Snyk 小 ，CVEurl_lis表示 vearcode
def case5_2(CVEurl_list, Snykurl_list):
    if not CVEurl_list:
        return False
    elif not Snykurl_list:
        return True
    else:
        CVEurl_list = sorted(set(CVEurl_list))
        NVDurl_list = sorted(set(Snykurl_list))
        for url in NVDurl_list:
            if url in CVEurl_list:
                continue
            else:
                return False
        return True

# Snyk 大
def case5_3(CVEurl_list, Snykurl_list):
    if not Snykurl_list:
        return False
    elif not CVEurl_list:
        return True
    else:
        CVEurl_list = sorted(set(CVEurl_list))
        Snykurl_list = sorted(set(Snykurl_list))
        for url in CVEurl_list:
            if url in Snykurl_list:
                continue
            else:
                return False
        return True



# # same set
# def case5_4(CVEurl_list, Snykurl_list):
#     if CVEurl_list and Snykurl_list: # 都不为None
#        if sorted( set(CVEurl_list) ) == sorted( set(Snykurl_list) ):
#            return True
#        else:
#            return False
#     elif not CVEurl_list and not Snykurl_list: # 都为None
#         return True
#     else: # other
#         return False

# * 6-1: upto CVEdetails Maximum 700
# * 6-2: range affected CPE version // 处理粗糙
# * 6-3: AND-OR // 处理粗糙
# * 6-4: Other

def case6_1(CVEdetailsVPV_list, NVDVPV_list):
    if CVEdetailsVPV_list and len( CVEdetailsVPV_list ) >= 674:
        return True
    else:
        return False

def case6_2(CVEdetailsVPV_list, NVDVPV_list,):
    pass

def case6_3(CVEdetailsVPV_list, NVDVPV_list):
    pass

def case6_4(CVEdetailsVPV_list, NVDVPV_list):
    pass


def main():
    global DifferenDataInfo, NVDvsCVEdetails_AnalysisData
    setMetadata()
    analyseData()
    JSONFIle_processing.write(json_content=NVDvsCVEdetails_AnalysisData.toDict(),path=NVDvsCVEdetails_DifferentAnalysis_path)


if __name__ == '__main__':
    main()