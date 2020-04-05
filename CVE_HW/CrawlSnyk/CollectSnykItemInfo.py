# -*- coding: utf-8 -*-

"""
Created on 2020-04-02 09:13  

@author: congyingxu
用于解析并收集所有SID的模块信息

Meta-Module：

Title
Affected package & Vesion
Overview
Details ：PoC by snyk有代码信息，json不太好存
Types of attacks
Affected environments
How to prevent
Remediation
Reference
Patch: from Reference Github commit / other forms?

CVSS Score & Vector

Credit ? is the same as CVE's contibutor
CVE
CWE
SNYK-ID
Disclosed Date
Published Data
"""

MavenItemPages_dir =  "/Users/congyingxu/Downloads/CVE/CrawledSnykHtmls/MavenItemPages/"
SnykItems_dir = "/Users/congyingxu/Downloads/CVE/CrawledSnykHtmls/SnykItems/"

SnykItemSIDData_path = '/Users/congyingxu/Downloads/CVE/CrawledSnykHtmls/SnykItemSIDData.json'
SnykItemSIDData = {}

SnykItemCVEData_path = '/Users/congyingxu/Downloads/CVE/CrawledSnykHtmls/SnykItemCVEData.json'
SnykItemCVEData = {}

None_CVE  = 0
Existing_CVE = 0