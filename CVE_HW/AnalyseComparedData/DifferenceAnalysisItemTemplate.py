# -*- coding: utf-8 -*-

"""
Created on 2020-04-18 10:47  

@author: congyingxu
"""

from CommonFunction import JSONFIle_processing



class DifferenceAnalysis:
    def __init__(self, DifferentData_path):
        # 文件信息啥的
        self.Path_DifferentData = DifferentData_path
        self.DifferenDataInfo = ''
        self.readDifferentData()

        # meta-data
        self.ComparedPart1_name = ''
        self.ComparedPart2_name = ''
        self.ComparedPart1_CVENum = ''
        self.ComparedPart2_CVENum = ''


        # 对比的CVE总量及不同量
        self.ComparedCVE_TotalNum = ''
        self.ComparedCVE_DiffNum = ''
        # 对比的Vector，及每个ele对应的C格式
        self.ComparedVector = '' # 存储 vector 和 case
        self.ComparedCase = ''  # case
        self.ComparedVector_CaseDifferentNums = '' # 存储数量
        self.ComparedVector_CaseDifferentCVEs = '' # 春初具体CVEID

        self.ComparedVector_FlagNums = {}  # 统计flag的数量
        self.ComparedVector_FlagCVEs = {}  # 统计flag对应的cve

        # 统计CVEID not in NVD 的情况
        self.NotComparedCVE_TotalNum = ''
        self.NotComparedCase = ''
        self.NotCompared_CaseNums = {}  # 存储数量
        self.NotCompared_CaseCVEs = {}  # 春初具体CVEID
        self.NotCompared_Annualprofile = {}  # 存储每年的数据情况



    def readDifferentData(self):
        self.DifferenDataInfo = JSONFIle_processing.read( self.Path_DifferentData )

    def extractDifferentData(self):
        pass

    def toDict(self):
        DictInfo = {}
        for name,value in vars(self).items():
            if name == 'DifferenDataInfo':
                continue
            DictInfo[name] = value
        return DictInfo
