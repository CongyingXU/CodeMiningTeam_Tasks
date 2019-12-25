#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 19:05:20 2019

@author: congyingxu

1、更新closed_issue
2、从issue的完整信息中摘取需要的信息 -> JIRA-3-No-Description
"""
import json
import os
from bs4 import BeautifulSoup

import time
log  = "\n\n\n=================================================================================" \
     + str(time.ctime()) +'\n' \
     +"新增项目['GROOVY','BEANUTILS','CONFIGURATION','DBCP','FILEUPLOAD','BVAL','COMPRESS','MATH','HADOOP','HTTPCORE','MNG','MPLUGIN','VELOCITY','ZOOKEEPER','HHH','JASSIST']"\
     +" （条件：closed bug & priority=critical/major/blocked & affection/fix version!=None） \n\n\n"


#Libraries = ['CLI','CODEC','COLLECTIONS','COMMON-IO','HTTPCLIENT','LANG','LOG4J2','LOGBACK','LOGGING','SLF4J']
Libraries = ['GROOVY','BEANUTILS','CONFIGURATION','DBCP','FILEUPLOAD','BVAL','COMPRESS','MATH','HADOOP','HTTPCORE','MNG','MPLUGIN'
             ,'VELOCITY','ZOOKEEPER','HHH','JASSIST']

#Libraries = ['GROOVY','BEANUTILS']


Stored_issues_dict = {}
Formatted_issues_dict = {"size":0}
count=0



def get_new_closed_issues(library):   
    global formated_issue_info,Stored_issues_dict,count,log
    
    path = 'Library_issue_information/'+library 
    if library == 'COMMON-IO':
        path ='Library_issue_information/'+'IO'
    
    
    issuesFiles_name = os.listdir(path)
    for issueF in issuesFiles_name:
        
    
        if issueF.endswith('Closed.txt') or issueF.endswith('Resolved.txt'):
            #获取issue信息
            issue_file =  open(path + '/' + issueF, 'r')
            #print issue_file.read() 
            try:
                issueJson = json.loads(issue_file.read())
            except ValueError:
                print (issueF,'ValueError')
                log +=issueF+' '+'ValueError\n'
            issue_file.close()
            
            
            if not Stored_issues_dict.has_key(library):#新增项目时，library不存在的
                Stored_issues_dict[library]= []
                
            
            #过滤HTTPCLIENT-800／804,因为它会跳转到 HTTPCORE
            key = issueJson["issue"]["key"]
            if key in Stored_issues_dict[library] or key =='HTTPCORE-174' or key=='HTTPCORE-175':
                continue
            
            issue_info_dict = {}
            html = issueJson["panels"]["leftPanels"][0]["html"]
            soup = BeautifulSoup(html, 'html.parser')
            #if issueF=='CLI-182_Closed.txt':
            soup.find_all('div')
            for ele in soup.find_all('div'):
                key_value =ele.text.replace('\n','').split(':')
                if len(key_value)==2:
                    issue_info_dict[key_value[0].strip(' ')] = key_value[1].strip(' ')
                   
                
            if not issue_info_dict['Type'] == "Bug":#标签为bug的issue
                continue
            
            #if issue_info_dict["Fix Version/s"]=='None':
            #    continue
              
            try:
                formated_issue_info = {}
                #status = issueJson["issue"]["status"]["name"]
                formated_issue_info['summary'] = issueJson["issue"]["summary"]
                formated_issue_info['key'] = key
                formated_issue_info['priority'] = issue_info_dict["Priority"]
                formated_issue_info['resolution'] = issue_info_dict["Resolution"]
                formated_issue_info['fixVersions'] = issue_info_dict["Fix Version/s"]
                formated_issue_info['affectsVersions'] = issue_info_dict["Affects Version/s"]
            except KeyError:#一些属性有问题了，这个issue就不用了
                print (key,'field error')
                continue
                
            
            try:#因为有的项目没有component
                formated_issue_info['components'] = issue_info_dict["Component/s"]
            except KeyError:
                formated_issue_info['components'] = 'None'
                #print issue_info_dict,key
            
            
            if formated_issue_info['fixVersions'] == 'None' or formated_issue_info['affectsVersions'] == 'None':
                continue
            #print issue_info_dict["Component/s"]
            if formated_issue_info['priority'] == 'Major' or formated_issue_info['priority'] == 'Blocker' or formated_issue_info['priority'] == 'Critical':
                
                #存入Stored_issues
                Stored_issues_dict[library].append(key)
                
                #存入formatted_issues
                affectsVersions_list = formated_issue_info['affectsVersions'].split(',')
                for ver in affectsVersions_list :
                    ver = ver.strip(' ')
                    #print ver,key
                    if ver=='None':
                        continue
                
                    if not Formatted_issues_dict.has_key(library+'_'+ver):#增加版本
                        Formatted_issues_dict[library+'_'+ver]={"bugs":[],"size":0}
                        print ("add version",ver,key,library+'_'+ver)
                        log +="add version,"+' '+str(ver)+' '+str(key)+' '+str(library)+'\n'
                        
                    
                    Formatted_issues_dict[library+'_'+ver]["bugs"].append(formated_issue_info)
                    Formatted_issues_dict[library+'_'+ver]["size"] +=1
                    Formatted_issues_dict["size"] +=1
                
                    print ('add',key,ver)
                    log += 'add'+' '+str(key)+'\n'
                    count +=1
            
        
def read_Stored_issues():
    global Stored_issues_dict
    Stored_issues_file =  open('JIRA-3-No-Desc/_Stored_issues.txt', 'r')            
    Stored_issues_dict = json.loads(Stored_issues_file.read())
    #print Stored_issues_dict
    Stored_issues_file.close()

def update_Stored_issues():
    global Stored_issues_dict,log
    f =  open('JIRA-3-No-Desc/_Stored_issues.txt', 'w')            
    f.write( json.dumps(Stored_issues_dict,indent=4) )
    f.close()
    
    f =  open('JIRA-3-No-Desc/_log.txt', 'a')            
    f.write( log )
    f.close()
       

def read_formatted_issues(library):
    global Formatted_issues_dict
    try:#当已有文件时
        formatted_issues_file =  open('JIRA-3-No-Desc/'+ library +'.txt', 'r')
        Formatted_issues_dict = json.loads(formatted_issues_file.read())
        #print Formatted_issues_dict
        formatted_issues_file.close()
    except IOError:
        print ('error'+library)
        Formatted_issues_dict={"size":0}
    


def update_formatted_issues(library):
    global Formatted_issues_dict
    f = open('JIRA-3-No-Desc/'+ library +'.txt', 'w')
    f.write( json.dumps(Formatted_issues_dict,indent=4) )
    f.close()


def main():
    read_Stored_issues()
    for library in Libraries:
        read_formatted_issues(library)
        get_new_closed_issues(library)
        update_formatted_issues(library)
        
    update_Stored_issues()
    print (count)
        
    
if __name__=='__main__':
    main()
