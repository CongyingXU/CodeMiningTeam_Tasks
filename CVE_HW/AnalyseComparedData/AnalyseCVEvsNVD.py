# -*- coding: utf-8 -*-

"""
Created on 2020-04-15 16:55  

@author: congyingxu
"""

from CommonFunction import JSONFIle_processing
from CVE_HW import CONFIG
from CVE_HW.CompareDataset import ParseCVEDictionary
from CVE_HW.AnalyseComparedData import DifferenceAnalysisItemTemplate


CVEDictionary_Instance = ParseCVEDictionary.CVEDictionary()
CVEvsNVDDifferentData_path = CONFIG.CVEvsNVD_Different_path
CVEvsNVD_DifferentAnalysis_path = CONFIG.CVEvsNVD_DifferentAnalysis_path



CVEvsNVD_AnalysisData =   DifferenceAnalysisItemTemplate.DifferenceAnalysis(CVEvsNVDDifferentData_path)

def analyseData():
    DifferenDataInfo = CVEvsNVD_AnalysisData.DifferenDataInfo

    # meta-data
    # self.ComparedPart1_name = ''
    # self.ComparedPart2_name = ''
    # self.ComparedPart1_CVENum = ''
    # self.ComparedPart2_CVENum = ''
    CVEvsNVD_AnalysisData.ComparedPart1_name = 'CVE'
    CVEvsNVD_AnalysisData.ComparedPart2_name = 'NVD'
    CVEvsNVD_AnalysisData.ComparedPart1_CVENum = '170801'
    CVEvsNVD_AnalysisData.ComparedPart2_CVENum = '139742'

    # # 对比的CVE总量及不同量
    # self.ComparedCVE_TotalNum = ''
    # self.ComparedCVE_DiffNum = ''
    CVEvsNVD_AnalysisData.ComparedCVE_TotalNum = 139742
    CVEvsNVD_AnalysisData.ComparedCVE_DiffNum = len(DifferenDataInfo.keys()) - 3  # 减去vector相关的那个, 3957


    # # 对比的Vector，及每个ele对应的C格式
    # self.ComparedVector = ''  # 存储 vector 和 case
    # self.ComparedVector_CaseDifferentNums = ''  # 存储数量
    # self.ComparedVector_CaseDifferentCVEs = ''  # 春初具体CVEID
    CVEvsNVD_AnalysisData.ComparedVector = ['1: desc', '2: refs',  '3: url_source']
    CVEvsNVD_AnalysisData.ComparedCase = ['1-1: Rejected in CVE and NVD','1-2: Rejected in CVE','1-3: Rejected in NVD', '1-4: Different description'
                                          '2-1: Reject in CVE',
                                          '2-2: same url set but with duplicate urls',
                                          '2-3: CVE lack ref', '2-4: NVD lack ref', '2-5: other',
                                          '3-1: Reject in CVE', '3-2: different url and different src',"3-3: same url but different src and somepart's src is N/A",
                                          '3-4: same url but different src', '3-5: other']
    CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentCVEs = {'1':[], '1-1':[], '1-2':[], '1-3':[], '1-4':[], '2':[], '2-1':[], '2-2':[], '2-3':[], '2-4':[], '2-5':[], '3':[], '3-1':[], '3-2':[], '3-3':[], '3-4':[], '3-5':[]}
    CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentNums = {'1':0, '1-1':0, '1-2':0, '1-3':0, '1-4':0, '2':0, '2-1':0, '2-2':0, '2-3':0, '2-4':0, '2-5':0, '3':0, '3-1':0, '3-2':0, '3-3':0, '3-4':0, '3-5':0}


    # self.NotComparedCVE_TotalNumandPartName = ''
    # self.NotComparedCase = ''
    # self.NotCompared_CaseNums = ''  # 存储数量
    # self.NotCompared_CaseCVEs = ''  # 春初具体CVEID
    CVEvsNVD_AnalysisData.NotComparedCVE_TotalNum = len( DifferenDataInfo['NotInNVDCVEIDs'] )
    CVEvsNVD_AnalysisData.NotComparedCase = ['#-1: Reserved CVEID: This candidate has been reserved by an organization or individual that will use it when announcing a new security problem. When the candidate has been publicized, the details for this candidate will be provided. ',
                                             "#-2: NVD's mistake: NVD fails to synchronize with CVE." ]
    CVEvsNVD_AnalysisData.NotCompared_CaseNums = {'#-1':0 , '#-2':0}  # 存储数量
    CVEvsNVD_AnalysisData.NotCompared_CaseCVEs = {'#-1':[] , '#-2':[]}  # 春初具体CVEID

    # analyse CVE Items not in NVD
    for CVEID in DifferenDataInfo['NotInNVDCVEIDs']:
        CVEID_Info = CVEDictionary_Instance.extractCVEitemInfo(CVEID)
        CVEID_desc = CVEID_Info[CVEID]['desc']
        CVEID_year = CVEID.split('-')[1]

        if CVEID_year in CVEvsNVD_AnalysisData.NotCompared_Annualprofile.keys():
            # print(CVEvsNVD_AnalysisData.NotCompared_Annualprofile[CVEID_year])
            CVEvsNVD_AnalysisData.NotCompared_Annualprofile[CVEID_year]['TotalNum'] += 1
            CVEvsNVD_AnalysisData.NotCompared_Annualprofile[CVEID_year]['AllCVEIDs'].append( [CVEID] )
        else:
            CVEvsNVD_AnalysisData.NotCompared_Annualprofile[CVEID_year] = {}
            CVEvsNVD_AnalysisData.NotCompared_Annualprofile[CVEID_year]['TotalNum'] = 1
            CVEvsNVD_AnalysisData.NotCompared_Annualprofile[CVEID_year]['#-1_Num'] = 0
            CVEvsNVD_AnalysisData.NotCompared_Annualprofile[CVEID_year]['#-2_Num'] = 0

            CVEvsNVD_AnalysisData.NotCompared_Annualprofile[CVEID_year]['AllCVEIDs'] = [CVEID]
            CVEvsNVD_AnalysisData.NotCompared_Annualprofile[CVEID_year]['#-1_CVEs'] = []
            CVEvsNVD_AnalysisData.NotCompared_Annualprofile[CVEID_year]['#-2_CVEs'] = []

        # case #-1
        if '** RESERVED **' in CVEID_desc:
            CVEvsNVD_AnalysisData.NotCompared_CaseNums['#-1'] += 1
            CVEvsNVD_AnalysisData.NotCompared_CaseCVEs['#-1'].append(CVEID)

            CVEvsNVD_AnalysisData.NotCompared_Annualprofile[CVEID_year]['#-1_Num'] += 1
            CVEvsNVD_AnalysisData.NotCompared_Annualprofile[CVEID_year]['#-1_CVEs'].append( CVEID )
        # case #-2
        elif len( CVEID_desc ) > 20:
            CVEvsNVD_AnalysisData.NotCompared_CaseNums['#-2'] += 1
            CVEvsNVD_AnalysisData.NotCompared_CaseCVEs['#-2'].append(CVEID)

            CVEvsNVD_AnalysisData.NotCompared_Annualprofile[CVEID_year]['#-2_Num'] += 1
            CVEvsNVD_AnalysisData.NotCompared_Annualprofile[CVEID_year]['#-2_CVEs'].append(CVEID)
        else:
            print(CVEID,CVEID_desc)


    # 汇总结果
    for CVEID_year in CVEvsNVD_AnalysisData.NotCompared_Annualprofile.keys():
        _1Num = CVEvsNVD_AnalysisData.NotCompared_Annualprofile[CVEID_year]['#-1_Num']
        _2Num = CVEvsNVD_AnalysisData.NotCompared_Annualprofile[CVEID_year]['#-2_Num']
        Total_Num = CVEvsNVD_AnalysisData.NotCompared_Annualprofile[CVEID_year]['TotalNum']

        CVEvsNVD_AnalysisData.NotCompared_Annualprofile[CVEID_year] = str(_1Num) + ' - ' + str(_2Num) + ' / ' + str(Total_Num)


    # analyse compared CVE Items
    for CVEID in  DifferenDataInfo.keys():
        if not CVEID.startswith('CVE-'):
            continue
        CVE_differentInfo = DifferenDataInfo[CVEID]
        flag = str(CVE_differentInfo['flag'])
        if flag in CVEvsNVD_AnalysisData.ComparedVector_FlagNums.keys():
            CVEvsNVD_AnalysisData.ComparedVector_FlagNums[flag] +=1
            CVEvsNVD_AnalysisData.ComparedVector_FlagCVEs[flag].append(CVEID)
        else:
            CVEvsNVD_AnalysisData.ComparedVector_FlagNums[flag] = 1
            CVEvsNVD_AnalysisData.ComparedVector_FlagCVEs[flag] = [CVEID]

        if '1' in flag:
            CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentNums['1'] += 1
            CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentCVEs['1'].append(CVEID)

            # 1-1 Reject
            if '** REJECT **' in CVE_differentInfo['CVE']['desc'] and '** REJECT **' in CVE_differentInfo['NVD']['desc']:
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentNums['1-1'] += 1
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentCVEs['1-1'].append(CVEID)
            elif '** REJECT **' in CVE_differentInfo['CVE']['desc']:
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentNums['1-2'] += 1
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentCVEs['1-2'].append(CVEID)
            elif '** REJECT **' in CVE_differentInfo['NVD']['desc']:
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentNums['1-3'] += 1
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentCVEs['1-3'].append(CVEID)
            # 1-2 Other
            else:
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentNums['1-4'] += 1
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentCVEs['1-4'].append(CVEID)

        if '2' in flag:
            CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentNums['2'] += 1
            CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentCVEs['2'].append(CVEID)

            CVEurl_list = [ele.split('__fdse__')[1] for ele in CVE_differentInfo['CVE']['refs']]
            NVDurl_list = [ele.split('__fdse__')[1] for ele in CVE_differentInfo['NVD']['refs']]
            CVEurlsrc_list = [ele.split('__fdse__')[0] for ele in CVE_differentInfo['CVE']['refs']]
            NVDurlsrc_list = [ele.split('__fdse__')[0] for ele in CVE_differentInfo['NVD']['refs']]
            # 2-1 Reject
            if '** REJECT **' in CVE_differentInfo['CVE']['desc']:
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentNums['2-1'] += 1
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentCVEs['2-1'].append(CVEID)
            # 2-2 CVE赘余，但其实一致
            elif case2_2(CVEurl_list, NVDurl_list):
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentNums['2-2'] += 1
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentCVEs['2-2'].append(CVEID)
            # 2-3 CVE缺失
            elif case2_3(CVEurl_list, NVDurl_list):
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentNums['2-3'] += 1
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentCVEs['2-3'].append(CVEID)
            # 2-4 NVD缺失
            elif case2_4(CVEurl_list, NVDurl_list):
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentNums['2-4'] += 1
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentCVEs['2-4'].append(CVEID)
            # 2-5 other:
            else:
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentNums['2-5'] += 1
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentCVEs['2-5'].append(CVEID)

        if '3' in flag:
            CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentNums['3'] += 1
            CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentCVEs['3'].append(CVEID)

            CVEurl_list = [ele.split('__fdse__')[1] for ele in CVE_differentInfo['CVE']['refs']]
            NVDurl_list = [ele.split('__fdse__')[1] for ele in CVE_differentInfo['NVD']['refs']]
            CVEurlsrc_list = [ele.split('__fdse__')[0] for ele in CVE_differentInfo['CVE']['refs']]
            NVDurlsrc_list = [ele.split('__fdse__')[0] for ele in CVE_differentInfo['NVD']['refs']]
            # 3-1 Reject
            if '** REJECT **' in CVE_differentInfo['CVE']['desc']:
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentNums['3-1'] += 1
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentCVEs['3-1'].append(CVEID)
            # 3-2: different url and different src
            elif case3_2(CVEurl_list,NVDurl_list,CVEurlsrc_list,NVDurlsrc_list):
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentNums['3-2'] += 1
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentCVEs['3-2'].append(CVEID)
            # 3-3: same url but somepart's src is N/A
            elif case3_3(CVEurl_list,NVDurl_list,CVEurlsrc_list,NVDurlsrc_list):
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentNums['3-3'] += 1
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentCVEs['3-3'].append(CVEID)
                #  因为3-3 属于3-4
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentNums['3-4'] += 1
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentCVEs['3-4'].append(CVEID)
            # 3-4: same url but different src （CVE vs NVD have same url num）
            elif case3_4(CVEurl_list,NVDurl_list,CVEurlsrc_list,NVDurlsrc_list):
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentNums['3-4'] += 1
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentCVEs['3-4'].append(CVEID)
            # # 3-5: same url but different src （CVE or NVD have duplicate url, but the url set is same）
            # elif case3_5(CVEurl_list,NVDurl_list,CVEurlsrc_list,NVDurlsrc_list):
            #     CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentNums['3-5'] += 1
            #     CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentCVEs['3-5'].append(CVEID)
            # other
            else:
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentNums['3-6'] += 1
                CVEvsNVD_AnalysisData.ComparedVector_CaseDifferentCVEs['3-6'].append(CVEID)

# 3-2: different url and different src
def case3_2(CVEurl_list,NVDurl_list,CVEurlsrc_list,NVDurlsrc_list):
    if sorted(set(CVEurl_list)) == sorted(set(NVDurl_list)):
        return False
    else:
        return True

# 3-3: same url but somepart's src is N/A
def case3_3(CVEurl_list,NVDurl_list,CVEurlsrc_list,NVDurlsrc_list):
    CVEurl_list = sorted(set(CVEurl_list))
    NVDurl_list = sorted(set(NVDurl_list))
    if CVEurl_list != NVDurl_list or len(CVEurl_list)!=len(CVEurlsrc_list):
        return False
    else:
        for index in range(len(CVEurlsrc_list)):
            CVEurlsrc = CVEurlsrc_list[index]
            NVDurlsrc = NVDurlsrc_list[index]
            if CVEurlsrc != NVDurlsrc_list and ( 'N/A' in CVEurlsrc or 'N/A' in NVDurlsrc):
                return True
        return False

# 3-4: same url but different src
def case3_4(CVEurl_list,NVDurl_list,CVEurlsrc_list,NVDurlsrc_list):
    CVEurl_list = sorted(set(CVEurl_list))
    NVDurl_list = sorted(set(NVDurl_list))
    if CVEurl_list == NVDurl_list:
        return True
    else:
        return False

# # 3-5: same url but different src （CVE vs NVD have different url num, but the url set is same,because CVE or NVD have duplicate url）
# def case3_5(CVEurl_list,NVDurl_list,CVEurlsrc_list,NVDurlsrc_list):
#     CVEurl_list = sorted(set(CVEurl_list))
#     NVDurl_list = sorted(set(NVDurl_list))
#     if CVEurl_list == NVDurl_list:
#         return True
#     else:
#         return False

def case2_2(CVEurl_list, NVDurl_list):
    # if len(CVEurl_list) != len(NVDurl_list):
       if sorted( set(CVEurl_list) ) == sorted( set(NVDurl_list) ):
           return True
       else:
           return False
    # else:
    #     return False

def case2_3(CVEurl_list, NVDurl_list):
    CVEurl_list = sorted(set(CVEurl_list))
    NVDurl_list = sorted(set(NVDurl_list))
    for url in CVEurl_list:
        if url in NVDurl_list:
            continue
        else:
            return False
    return True


def case2_4(CVEurl_list, NVDurl_list):
    CVEurl_list = sorted(set(CVEurl_list))
    NVDurl_list = sorted(set(NVDurl_list))
    for url in NVDurl_list:
        if url in CVEurl_list:
            continue
        else:
            return False
    return True

def case2_5(CVEurl_list, NVDurl_list):
    CVEurl_list = sorted(set(CVEurl_list))
    NVDurl_list = sorted(set(NVDurl_list))
    pass


def main():
    global CVEvsNVD_AnalysisData
    analyseData()
    JSONFIle_processing.write(json_content=CVEvsNVD_AnalysisData.toDict(),path=CVEvsNVD_DifferentAnalysis_path)


if __name__ == '__main__':
    main()