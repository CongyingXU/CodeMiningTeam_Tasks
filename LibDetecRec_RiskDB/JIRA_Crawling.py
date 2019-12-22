#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 16:26:02 2019

@author: congyingxu
"""
import json


import requests
from bs4 import BeautifulSoup

GA_IssueKey_name = 'HADOOP'

issueKeys_list = []
first_issuekey = ''

issue_information_url = 'https://issues.apache.org/jira/secure/AjaxIssueAction!default.jspa?issueKey=%s&decorator=none&prefetch=false&shouldUpdateCurrentProject=false&loadFields=false&'
# informaton in json
project_url = 'https://issues.apache.org/jira/issues/?jql=project%20%3D%20' + GA_IssueKey_name
#Path = u'/Users/congyingxu/Desktop/陈老师课题组/Library_issue_information/'+ project
Path = '' + GA_IssueKey_name
GA_Track_dict ={}
lib_IssuekeyName_Map = {'hadoop':'HADOOP'}

def init(GA_lib):
    global GA_IssueKey_name,issueKeys_list, project_url, first_issuekey,GA_Track_dict


    with open('../GA-Tracker-Map.json','r') as f:
        data_dict = json.loads(f.read())
        for ele in data_dict:
            GA = data_dict['groupId']+'__fdse__'+data_dict['artifactId']
            GA_Track_dict[GA] = data_dict['trackerUrl']


    GA_IssueKey_name = lib_IssuekeyName_Map[GA_lib]

    issueKeys_list = []
    first_issuekey = ''

    issue_information_url = 'https://issues.apache.org/jira/secure/AjaxIssueAction!default.jspa?issueKey=%s&decorator=none&prefetch=false&shouldUpdateCurrentProject=false&loadFields=false&'
    # informaton in json
    # project_url = 'https://issues.apache.org/jira/issues/?jql=project%20%3D%20' + GA_IssueKey_name
    project_url = GA_Track_dict[GA_lib]
    # Path = u'/Users/congyingxu/Desktop/陈老师课题组/Library_issue_information/'+ project
    Path = '' + GA_IssueKey_name


def get_issueKeys_list():
    
    global issueKeys_list,project_url,first_issuekey
    
    response = requests.get(project_url)
    response.encoding = 'utf-8'
    
    #print(response.text)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find('div',attrs={'class':"navigator-content"})
    a =  div.attrs['data-issue-table-model-state'] 
    a = json.loads(a)
    issueKeys_list =  a['issueTable']['issueKeys']
    
    first_issuekey = issueKeys_list[0]
    print( 'first_issuekey',first_issuekey )
    

def craw_write():
    global issueKeys_list,issue_information_url
    # for issuekey in issueKeys_list:
    #for issuekey in issueKeys_list[-660:]:   #当中途异常中断时，根据issuekey，粗略逆推  再次爬取的开始点
    #num = int(first_issuekey.split('-')[1])
    # num = 3521
    # while num>0:
    #     issuekey = GA_lib + '-' + str(num)
    #     num = num-1
    for issuekey in issueKeys_list:

        real_issue_information_url = issue_information_url % issuekey
        response = requests.get(real_issue_information_url)
        response.encoding = 'utf-8'
        info_dict = json.loads(response.text)
        try:
            status = info_dict['issue']['status']['name']
        except KeyError:
            print( issuekey,'not exist' )
            continue
        
        filePath = Path +'/'+ issuekey+'_'+ status+'.txt'
        f = open(filePath, 'w')
        f.write(json.dumps(info_dict, indent=4))
        
        # f.write('\n')
        print( issuekey )
        
if __name__=='__main__':
    GA_lib = 'commons-cli__fdse__commons-cli'
    get_issueKeys_list(GA_lib)
    craw_write()
    





