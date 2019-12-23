#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 16:26:02 2019

@author: congyingxu
"""
import os,json,sqlite3
import requests
from bs4 import BeautifulSoup

#变化项目：
project_list = [] #[{poj_git_name:{'jira_url_value':jira_url,'issue_name_prefix_value':issue_name_prefix_value}} , {} , {}]
issue_name_prefix = 'CLI'
issueKeys_list = []
first_issuekey = ''

#默认不便项目
issue_information_url = 'https://issues.apache.org/jira/secure/AjaxIssueAction!default.jspa?issueKey=%s&decorator=none&prefetch=false&shouldUpdateCurrentProject=false&loadFields=false&'
DB_path = 'RISK_DB.sqlite'
project_url = 'https://issues.apache.org/jira/issues/?jql=project%20%3D%20'
Path = 'CrawledIssues/'
# real_issue_information_url = issue_information_url % issuekey
# project_url = 'https://issues.apache.org/jira/issues/?jql=project%20%3D%20' + GA_IssueKey_name
# Path = 'CrawledIssues/' + issue_name_prefix


def read_info():
    # 连接到数据库
    # 数据库文件是“test.db”
    # 如果数据库不存在的话，将会自动创建一个 数据库
    conn = sqlite3.connect(DB_path)

    # 创建一个游标 curson
    cursor = conn.cursor()

    # 执行一条语句,创建 user表
    # sql = "create table login (id varchar(20) primary key, name varchar(30), password varchar(30))"
    # cursor.execute(sql)

    # 插入一条记录
    # sql = "insert into login (name, password) values (\'love\', \'520520')"
    # cursor.execute(sql)

    # 查询一条记录：
    sql = "select * from group_artifact_issue_map"
    cursor.execute(sql)
    # sql = "select * from group_artifact_issue_map where id=?"
    # cursor.execute(sql, ("2",))

    # 获取查询结果：
    values = cursor.fetchall() #返回最终一次sql结果，列表元组形式   #[(1, 'ch.qos.logback', .....), (2, 'commons-cli', ...)]

    for ele in values:
        git_name_value = ele[3]
        issue_name_prefix_value = ele[5]
        jira_url_value = ele[6]

        project_list.append({'git_name_value':git_name_value,'issue_name_prefix_value':issue_name_prefix_value,'jira_url_value':jira_url_value})
    print(project_list)

    # 通过rowcount获得插入的行数:
    # cursor.rowcount()

    # 关闭游标：
    cursor.close()

    # 提交事物
    conn.commit()

    # 关闭连接
    conn.close()

def init(poj_info):
    global issue_name_prefix, project_url,Path

    issue_name_prefix = poj_info['issue_name_prefix_value']
    jira_url = poj_info['jira_url_value']

    # issue_information_url = 'https://issues.apache.org/jira/secure/AjaxIssueAction!default.jspa?issueKey=%s&decorator=none&prefetch=false&shouldUpdateCurrentProject=false&loadFields=false&'
    # project_url = 'https://issues.apache.org/jira/issues/?jql=project%20%3D%20' + issue_name_prefix
    project_url = jira_url
    Path = Path + issue_name_prefix


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
    global issueKeys_list,issue_information_url,issue_name_prefix
    # for issuekey in issueKeys_list:
    #for issuekey in issueKeys_list[-660:]:   #当中途异常中断时，根据issuekey，粗略逆推  再次爬取的开始点
    num = int(first_issuekey.split('-')[1]) #当中途异常中断时，根据issuekey，粗略逆推  再次爬取的开始点
    # num = 3521
    while num>0:
        issuekey = issue_name_prefix + '-' + str(num)
        num = num-1

        real_issue_information_url = issue_information_url % issuekey
        response = requests.get(real_issue_information_url)
        response.encoding = 'utf-8'
        info_dict = json.loads(response.text)
        try:
            status = info_dict['issue']['status']['name']
        except KeyError:
            print( issuekey,'not exist' )
            continue
        if os.path.exists(Path):
            pass
        else:
            os.mkdir(Path)
        filePath = Path +'/'+ issuekey+'_'+ status+'.txt'
        f = open(filePath, 'w')
        f.write(json.dumps(info_dict, indent=4))
        
        # f.write('\n')
        print( issuekey )

def main():
    read_info() # 得到有待爬取的poj poj_list等信息
    for poj_info in project_list[1:]:
        init(poj_info) # 针对某个poj，初始化相关信息
        get_issueKeys_list()
        craw_write()

if __name__=='__main__':
    main()
    # init()  # 针对某个poj，初始化相关信息
    # get_issueKeys_list()
    # craw_write()
    





