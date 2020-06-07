# -*- coding: utf-8 -*-

"""
Created on 2020-04-06 16:12  

@author: congyingxu
"""

class CVEItem:

    def __init__(self):
        self.ItemPath  = ''
        self.CVEID = ''
        self.Description  = ''
        self.Reference = ''
        self.CVSS2 = ''
        self.CVSS3 = ''
        self.CVSS2Vector = ''
        self.CVSS3Vector = ''
        self.CWE = ''
        self.AffectedVendorProductCPE = ''
        self.AffectedVendorProductVersionCPE = ''

        self.Language  =''
        self.Patch = ''
        self.OvalDefinition = ''

        # tag
        self.tag_ANDOR = ''
        self.tag_CpeRange = ''

    def toDict(self):
        # item  = {}
        # item['ItemPath'] = self.ItemPath
        # item['CVEID'] = self.CVEID
        # item['Description'] = self.Description
        # item['Reference'] = self.Reference
        # item['CVSS2'] = self.CVSS2
        # item['CVSS3'] = self.CVSS3
        # item['CVSS2Vector'] = self.CVSS2Vector
        # item['CVSS3Vector'] = self.CVSS3Vector
        # item['CWE'] = self.CWE
        # item['AffectedVendorProductCPE'] = self.AffectedVendorProductCPE
        #
        # item['AffectedVendorProductCPE'] = self.AffectedVendorProductCPE
        # item['AffectedVendorProductVersionCPE'] = self.AffectedVendorProductVersionCPE
        # item['Language'] = self.Language
        # item['Patch'] = self.Patch
        # item['OvalDefinition'] = self.OvalDefinition
        #
        # return item
        DictInfo = {}
        for name, value in vars(self).items():
            if name == 'DifferenDataInfo':
                continue
            DictInfo[name] = value
        return DictInfo