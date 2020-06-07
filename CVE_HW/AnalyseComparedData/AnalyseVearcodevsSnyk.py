# -*- coding: utf-8 -*-

"""
Created on 2020-04-18 10:22  

@author: congyingxu
"""

from CommonFunction import JSONFIle_processing

from CVE_HW.AnalyseComparedData import DifferenceAnalysisItemTemplate
from CVE_HW import CONFIG


SnykvsVearcode_DifferentAnalysis_path = CONFIG.SnykvsVearcode_DifferentAnalysis_path
SnykvsVearcodeDifferentData_path = CONFIG.SnykvsVearcode_Different_path
SnykvsVearcode_AnalysisData =   DifferenceAnalysisItemTemplate.DifferenceAnalysis(SnykvsVearcodeDifferentData_path)

DifferenDataInfo = SnykvsVearcode_AnalysisData.DifferenDataInfo


def setMetadata():
    global DifferenDataInfo, SnykvsVearcode_AnalysisData

    # meta-data
    # self.ComparedPart1_name = ''
    # self.ComparedPart2_name = ''
    # self.ComparedPart1_CVENum = ''
    # self.ComparedPart2_CVENum = ''
    SnykvsVearcode_AnalysisData.ComparedPart1_name = 'Snyk'
    SnykvsVearcode_AnalysisData.ComparedPart2_name = 'Vearcode'
    SnykvsVearcode_AnalysisData.ComparedPart1_CVENum = '6088'
    SnykvsVearcode_AnalysisData.ComparedPart2_CVENum = '8895'

    # # 对比的CVE总量及不同量
    # self.ComparedCVE_TotalNum = ''
    # self.ComparedCVE_DiffNum = ''
    SnykvsVearcode_AnalysisData.ComparedCVE_TotalNum = len( DifferenDataInfo['ComparedCVEIDs'] )
    SnykvsVearcode_AnalysisData.ComparedCVE_DiffNum = len(DifferenDataInfo.keys()) - 4  # 减去vector相关的那个, 72093

    # # 对比的Vector，及每个ele对应的C格式
    # self.ComparedVector = ''  # 存储 vector 和 case
    # self.ComparedVector_CaseDifferentNums = ''  # 存储数量
    # self.ComparedVector_CaseDifferentCVEs = ''  # 春初具体CVEID
    SnykvsVearcode_AnalysisData.ComparedVector = ['1 language', '2 refs','3 patch', '4 Affected package' ]
    SnykvsVearcode_AnalysisData.ComparedCase = ['2-1: Different set','2-2: Vearcode is subset', '2-3: Snyk is subset', '2-4: Same set',
                                                '3-1: Different set','3-2: Vearcode is subset', '3-3: Snyk is subset',
                                                '#3-4: Total ComparedCVEnum with patch','#3-5: SnykCVEnum with patch','#3-6: VearcodeCVEnum with patch',
                                                '4-1: Different set', '4-2: Vearcode is the subset', '4-3: Snyk is the subset', '2-4: Same set' ]

    SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentCVEs = {'1': [],
                                                                     '2':[], '2-1':[], '2-2':[], '2-3':[], '2-4':[],
                                                                     '3':[], '3-1':[], '3-2':[], '3-3':[], '# 3-4':[],'# 3-5':[],'# 3-6':[],
                                                                     '4':[], '4-1':[], '4-2':[], '4-3':[], '4-4':[],
                                                                     }
    SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentNums = {'1': 0,
                                                                    '2': 0, '2-1': 0, '2-2': 0, '2-3': 0, '2-4': 0,
                                                                    '3': 0, '3-1': 0, '3-2': 0, '3-3': 0, '# 3-4': 0, '# 3-5':0,'# 3-6':0,
                                                                    '4': 0, '4-1': 0, '4-2': 0, '4-3': 0, '4-4': 0,
                                                                    }


    # self.NotComparedCVE_TotalNumandPartName = ''
    # self.NotComparedCase = ''
    # self.NotCompared_CaseNums = ''  # 存储数量
    # self.NotCompared_CaseCVEs = ''  # 春初具体CVEID
    SnykvsVearcode_AnalysisData.NotComparedCVE_TotalNum = 'Snyk:' + str(len(DifferenDataInfo['NotInSnykCVEIDs'])) + '  Vearcode:' + str(len(DifferenDataInfo['NotInVearcodeCVEIDs']))
    SnykvsVearcode_AnalysisData.NotComparedCase = [
        '#-1: Not in Vearcode and not in Snyk',
        '#-2: Not in Vearcode but in Snyk',
        '#-3: In Vearcode but not in Snyk']
    SnykvsVearcode_AnalysisData.NotCompared_CaseNums = {'#-1': 0, '#-2': 0, '#-3': 0}  # 存储数量
    SnykvsVearcode_AnalysisData.NotCompared_CaseCVEs = {'#-1': [], '#-2': [], '#-3': []}  # 春初具体CVEID


def analyseData():
    global DifferenDataInfo, SnykvsVearcode_AnalysisData

    # analyse CVE not in Snyk / Vearcode
    NotInSnyk_set  = set( DifferenDataInfo['NotInSnykCVEIDs'] )
    NotInVearcode_set = set( DifferenDataInfo['NotInVearcodeCVEIDs'] )
    # 全集
    NotInUnion_list = list( NotInSnyk_set.union(NotInVearcode_set))
    SnykvsVearcode_AnalysisData.NotCompared_CaseNums['#-1'] = len( NotInUnion_list )
    SnykvsVearcode_AnalysisData.NotCompared_CaseCVEs['#-1'] = NotInUnion_list
    # Vearcode 补集
    NotInVearcodeDifference_list = list( NotInVearcode_set.difference(NotInSnyk_set)  )
    SnykvsVearcode_AnalysisData.NotCompared_CaseNums['#-2'] = len(NotInVearcodeDifference_list)
    SnykvsVearcode_AnalysisData.NotCompared_CaseCVEs['#-2'] = NotInVearcodeDifference_list
    # Snyk 补集
    NotInSnykDifference_list = list(NotInSnyk_set.difference(NotInVearcode_set))
    SnykvsVearcode_AnalysisData.NotCompared_CaseNums['#-3'] = len(NotInSnykDifference_list)
    SnykvsVearcode_AnalysisData.NotCompared_CaseCVEs['#-3'] = NotInSnykDifference_list


    # 3 - 4~6
    # analyse ComparedCVE with patch in Snyk / Vearcode
    SnykCVEPatch_set = set(DifferenDataInfo['ComparedSnykCVEwithPatch'])
    VearcodeCVEPatch_set = set(DifferenDataInfo['ComparedVearcodeCVEwithPatch'])
    # 全集
    CVEPatchUnion_list = list(SnykCVEPatch_set.union(VearcodeCVEPatch_set))
    SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentNums['# 3-4'] = len(CVEPatchUnion_list)
    SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentCVEs['# 3-4'] = CVEPatchUnion_list

    # SnykCVEPatch_set
    SnykCVEPatch_set = list(SnykCVEPatch_set)
    SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentNums['# 3-5'] = len(SnykCVEPatch_set)
    SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentCVEs['# 3-5'] = SnykCVEPatch_set
    # VearcodeCVEPatch_set
    VearcodeCVEPatch_set = list(VearcodeCVEPatch_set)
    SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentNums['# 3-6'] = len(VearcodeCVEPatch_set)
    SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentCVEs['# 3-6'] = VearcodeCVEPatch_set


    # analyse compared CVE Items
    for CVEID in DifferenDataInfo.keys():
        if not CVEID.startswith('CVE-'):
            continue
        print(CVEID)
        # CVEID = 'CVE-2014-9809'
        CVE_differentInfo = DifferenDataInfo[CVEID]
        flag = str(CVE_differentInfo['flag'])
        if flag in SnykvsVearcode_AnalysisData.ComparedVector_FlagNums.keys():
            SnykvsVearcode_AnalysisData.ComparedVector_FlagNums[flag] += 1
            SnykvsVearcode_AnalysisData.ComparedVector_FlagCVEs[flag].append(CVEID)
        else:
            SnykvsVearcode_AnalysisData.ComparedVector_FlagNums[flag] = 1
            SnykvsVearcode_AnalysisData.ComparedVector_FlagCVEs[flag] = [CVEID]

        if '1' in flag:
            SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentNums['1'] += 1
            SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentCVEs['1'].append(CVEID)
            pass

        if '2' in flag:
            SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentNums['2'] += 1
            SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentCVEs['2'].append(CVEID)

            Vearcode_list = CVE_differentInfo['Vearcode']['Reference']
            Snyk_list = CVE_differentInfo['Snyk']['Reference']
            # 2-1
            if case2_1(Vearcode_list,Snyk_list):
                SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentNums['2-1'] += 1
                SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentCVEs['2-1'].append(CVEID)
            # 2-2 same url set but with duplicate urls
            elif case2_2(Vearcode_list,Snyk_list):
                SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentNums['2-2'] += 1
                SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentCVEs['2-2'].append(CVEID)
            # 2-3 CVE缺失
            elif case2_3(Vearcode_list,Snyk_list):
                SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentNums['2-3'] += 1
                SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentCVEs['2-3'].append(CVEID)
            elif case2_4(Vearcode_list, Snyk_list):
                SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentNums['2-4'] += 1
                SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentCVEs['2-4'].append(CVEID)
            else:
                print('Buyingdang')

        # patch
        if '3' in flag:
            SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentNums['3'] += 1
            SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentCVEs['3'].append(CVEID)

            Vearcode_list = CVE_differentInfo['Vearcode']['Patch']
            Snyk_list = CVE_differentInfo['Snyk']['Patch']
            # 2-1

            # 2-2 same url set but with duplicate urls
            if case2_2(Vearcode_list, Snyk_list):
                SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentNums['3-2'] += 1
                SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentCVEs['3-2'].append(CVEID)
            # 2-3 CVE缺失
            elif case2_3(Vearcode_list, Snyk_list):
                SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentNums['3-3'] += 1
                SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentCVEs['3-3'].append(CVEID)

            elif case2_1(Vearcode_list, Snyk_list):
                SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentNums['3-1'] += 1
                SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentCVEs['3-1'].append(CVEID)
            else:
                print('Buyingdang')

        # affected package
        if '4' in flag:
            SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentNums['4'] += 1
            SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentCVEs['4'].append(CVEID)

            Vearcode_list = CVE_differentInfo['Vearcode']['AffectedVendorProductCPE']
            Snyk_list = CVE_differentInfo['Snyk']['AffectedVendorProductCPE']
            # 2-1
            if case2_1(Vearcode_list, Snyk_list):
                SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentNums['4-1'] += 1
                SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentCVEs['4-1'].append(CVEID)
            # 2-2 same url set but with duplicate urls
            elif case2_2(Vearcode_list, Snyk_list):
                SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentNums['4-2'] += 1
                SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentCVEs['4-2'].append(CVEID)
            # 2-3 CVE缺失
            elif case2_3(Vearcode_list, Snyk_list):
                SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentNums['4-3'] += 1
                SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentCVEs['4-3'].append(CVEID)
            elif case2_4(Vearcode_list, Snyk_list):
                SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentNums['4-4'] += 1
                SnykvsVearcode_AnalysisData.ComparedVector_CaseDifferentCVEs['4-4'].append(CVEID)
            else:
                print('Buyingdang')


# different set
def case2_1(CVEurl_list, Snykurl_list):
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



# Snyk 大
def case2_2(CVEurl_list, Snykurl_list):
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

# Snyk 小 ，CVEurl_lis表示 vearcode
def case2_3(CVEurl_list, Snykurl_list):
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

# same set
def case2_4(CVEurl_list, Snykurl_list):
    if CVEurl_list and Snykurl_list: # 都不为None
       if sorted( set(CVEurl_list) ) == sorted( set(Snykurl_list) ):
           return True
       else:
           return False
    elif not CVEurl_list and not Snykurl_list: # 都为None
        return True
    else: # other
        return False


def main():
    global DifferenDataInfo, SnykvsVearcode_AnalysisData
    setMetadata()
    analyseData()
    JSONFIle_processing.write(json_content=SnykvsVearcode_AnalysisData.toDict(),path=SnykvsVearcode_DifferentAnalysis_path)


if __name__ == '__main__':
    main()