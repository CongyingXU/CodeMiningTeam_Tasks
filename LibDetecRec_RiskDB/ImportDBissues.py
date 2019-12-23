# -*- coding: utf-8 -*-

"""
Created on 2019-12-23 12:03  

@author: congyingxu

将爬取的issue信息，导入db中的issue
"""
import os,json
from bs4 import BeautifulSoup
import sqlite3

CrawledIssuesFloder_path = 'CrawledIssues/'
DB_path = 'RISK_DB.sqlite'
pojIssuePrefix_list = []
issuefile_list = []



def get_pojlist(): #读取crawledIssues中的文件夹，已确定待入库的poj
    global poj_list
    for parent, dirnames, filenames in os.walk(CrawledIssuesFloder_path):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            poj_list = dirnames

def get_issuefiles_list(pojpath):
    global issuefile_list
    for parent, dirnames, filenames in os.walk(pojpath):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        issuefile_list = filenames





def importIssuesInfo(filepath):
    with open(filepath, 'r') as f:
        issueJson = json.loads(f.read())

    key = issueJson["issue"]["key"]
    issue_info_dict = {}
    html = issueJson["panels"]["leftPanels"][0]["html"]
    soup = BeautifulSoup(html, 'html.parser')
    soup.find_all('div')
    for ele in soup.find_all('div'):
        key_value = ele.text.replace('\n', '').split(':')
        if len(key_value) == 2:
            issue_info_dict[key_value[0].strip(' ')] = key_value[1].strip(' ')

    # if not issue_info_dict['Type'] == "Bug":  # 标签为bug的issue,
    #     return

    try:
        formated_issue_info = {}
        formated_issue_info['status'] = issueJson["issue"]["status"]["name"]
        formated_issue_info['summary'] = issueJson["issue"]["summary"]
        formated_issue_info['key'] = key
        formated_issue_info['priority'] = issue_info_dict["Priority"]
        formated_issue_info['resolution'] = issue_info_dict["Resolution"]
        formated_issue_info['fixVersions'] = issue_info_dict["Fix Version/s"]
        formated_issue_info['affectsVersions'] = issue_info_dict["Affects Version/s"]
    except KeyError:  # 一些属性有问题了，这个issue就不用了
        print(key, 'field error')

    insertRecord(formated_issue_info)

def insertRecord(formated_issue_info):
    issuekey = formated_issue_info['key']
    status = formated_issue_info['status']
    affectsVersions = formated_issue_info['affectsVersions']
    summary = formated_issue_info['summary']
    issue_name_prefix = issuekey.split('-')[0]

    # 检查是否存在
    # 已存在的话则删除？且重新导入
    # 连接到数据库
    # 数据库文件是“test.db”
    # 如果数据库不存在的话，将会自动创建一个 数据库
    conn = sqlite3.connect(DB_path)
    # 创建一个游标 curson
    cursor = conn.cursor()

    # 查询一条记录：
    # sql = "select * from issues"
    # cursor.execute(sql)
    sql = "select * from issues where issue_key=?"
    cursor.execute(sql, (issuekey,))

    # 获取查询结果：
    values = cursor.fetchall()  # 返回最终一次sql结果，列表元组形式   #[(1, 'ch.qos.logback', .....), (2, 'commons-cli', ...)]
    if len(values) > 0: #有
        pre_status = values[0][5]
        if pre_status == status: #status没变
            pass
        else: # 修改旧的记录
            pre_id = values[0][0]
            sql = "UPDATE issues set affect_version = ? summary = ?status = ? where ID=?"
            cursor.execute(sql, (affectsVersions,summary,pre_id))

    else: # 增加记录
        sql = "insert into issues (issue_name_prefix,issue_key,affect_version,summary,status) values (?,?,?,?,?)"
        cursor.execute(sql,(issue_name_prefix,issuekey,affectsVersions,summary,status,))


    # 关闭游标：
    cursor.close()

    # 提交事物
    conn.commit()

    # 关闭连接
    conn.close()


def main():
    get_pojlist()
    for pojIssuePrefix in pojIssuePrefix_list:
        path = CrawledIssuesFloder_path + pojIssuePrefix
        importIssuesInfo()

if __name__ == '__main__':
    # main()
    importIssuesInfo('CrawledIssues/CLI/CLI-294_Resolved.txt')