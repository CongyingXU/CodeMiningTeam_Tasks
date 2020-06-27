# -*- coding: utf-8 -*-

"""
Created on 2020-04-06 17:00  

@author: congyingxu
"""

# root_dir = "/home/hadoop/dfs/data/Workspace/CongyingXU/"
root_dir = "/Volumes/MyPassport/"

# chromedriver
ChromeDriver_path =  '/Users/congyingxu/Documents/chromedriver'

# CVE
CVE_CVEID_list_dir = root_dir + 'CVE/MetaData/CVE_CVEID_list.json'
CVE_dataset_file_path =  root_dir + 'CVE/DataSet-CVE_MITRE/allitems.xml'
CVEItems_dir =  root_dir + 'CVE/DataSet-CVE_MITRE/CVEItems/'



# CVEdetails
CVEdetialsItems_dir = root_dir + 'CVE/CrawledCVEdetailsHtmls/CVEDetailsItems/'
CVEDetails_CVEID_list_path = root_dir + 'CVE/MetaData/CVEDetails_CVEID_list.json'
CVEDetails_pages_dir = root_dir + 'CVE/CrawledCVEdetailsHtmls/Pages/'


# NVD
NVD_CVEID_list_path = root_dir + "CVE/MetaData/NVD_CVEID_list.json"
NVDCperange_html_dir = root_dir + "CVE/DataSet-NVD/NVDCpeRange/htmls/"
NVDCperange_items_dir = root_dir + "CVE/DataSet-NVD/NVDCpeRange/items/"
NVDDataset_dir = root_dir + "CVE/DataSet-NVD/"
NVDItems_dir = root_dir + "CVE/DataSet-NVD/NVDItems/"
NVD_NoCpeRange_list_path = root_dir + "CVE/DataSet-NVD/NVD_NoCpeRange_list.json"
NVD_CpeANDOR_list_path = root_dir + "CVE/DataSet-NVD/NVD_CpeANDOR_list.json"
NVD_CpeRange_items_dir = root_dir + "CVE/DataSet-NVD/NVDCpeRange/items/"

# Vearcode
VearCodeCrawledVearCodeHtmls_dir = root_dir + "CVE/CrawledVearCodeHtmls/"
VearCodeLanguageVulnerList_dir = root_dir + "CVE/CrawledVearCodeHtmls/LanguageVulnerList/"
VearCodeItems_dir = root_dir + "CVE/CrawledVearCodeHtmls/VearCodeItems/"
VearCodeArtifact_dir = root_dir + "CVE/CrawledVearCodeHtmls/VearCodeArtifacts/"
VearCodelanguage_list = ['swift', 'os', 'csharp', 'php', 'go', 'objectivec', 'ruby', 'cpp', 'python', 'javascript', 'java']

Vearcode_Profile_path = root_dir + "CVE/CrawledVearCodeHtmls/VearcodeDataSetProfile.json"

VearcodeLanguageItemSID_list_path = root_dir + "CVE/CrawledVearCodeHtmls/LanguageVearcodeItemSID_list.json"
VearcodeLanguageCVEVearcodeItemSID_map_path = root_dir + "CVE/CrawledVearCodeHtmls/LanguageCVEVearcodeItemSID_map.json"


# Snyk
Snyk_page_store_dir = root_dir + "CVE/CrawledSnykHtmls/SnkyItemPages/"
Snyk_Snky_item_list_path = root_dir + "CVE/CrawledSnykHtmls/Snyk_id_Lists.json"
Snyk_item_data_path = root_dir + "CVE/CrawledSnykHtmls/SnykItemInfo.json"
Snyk_vuln_lib_data_path = root_dir + "CVE/CrawledSnykHtmls/Snyk_vuln_lib.json"

Snyk_ItemPages_dir = root_dir + "CVE/CrawledSnykHtmls/SnkyItemPages/"
SnykItems_dir = root_dir + "CVE/CrawledSnykHtmls/SnykItems/"
Snyk_LanguageItemSID_list_path = root_dir + "CVE/CrawledSnykHtmls/LanguageSnykItemSID_list.json"
Snyk_LanguageCVESnykItemID_map_path = root_dir + "CVE/CrawledSnykHtmls/LanguageCVESnykItemID_map.json"
Snyk_ItemID_list_path = root_dir + "CVE/CrawledSnykHtmls/Snyk_id_Lists.json"


# NVD vs CVEdetails
NVDvsCVEdetails_Different_path = root_dir + "CVE/NVDvsCVEdetails_Different.json"
NVDvsCVEdetails_DifferentAnalysis_path = root_dir + "CVE/NVDvsCVEdetails_DifferentAnalysis.json"

SnykvsVearcode_Different_path = root_dir + "CVE/SnykvsVearcode_Different.json"
SnykvsVearcode_DifferentAnalysis_path = root_dir + "CVE/SnykvsVearcode_DifferentAnalysis.json"

CVEvsNVD_Different_path = root_dir + "CVE/CVEvsNVD_Different.json"
CVEvsNVD_DifferentAnalysis_path = root_dir + "CVE/CVEvsNVD_DifferentAnalysis.json"

