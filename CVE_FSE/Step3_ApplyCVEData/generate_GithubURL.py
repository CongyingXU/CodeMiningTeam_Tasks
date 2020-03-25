# -*- coding: utf-8 -*-

"""
Created on 2020-02-28 21:38  

@author: congyingxu
"""
from CommonFunction import File_processing, JSONFIle_processing


path = "/Users/congyingxu/Downloads/disabled/"

file_list = File_processing.walk_L1_FileNames(path)

print(file_list)
issule_info = JSONFIle_processing.read("issue_info.json")
log = JSONFIle_processing.read('issue_log.json')

GA_url = JSONFIle_processing.read("/Users/congyingxu/Downloads/issue_disabled.json")
for GA in GA_url.keys():
    if GA in log or GA_url[GA] == '':
        continue



    try:
        # url = "https://github.com/" + file.split("__fdse__")[0] +'/'+file.split("__fdse__")[1].strip('.md') +'/'+ 'issues'
        url = GA_url[GA]
    except:
        continue
    print(GA)
    print(url)
    print( "-------------------------------------------------------------------------")

    with open(path+GA+'.md','r') as f:
        print(f.read().replace('*',''))

    item = {}
    item["proj_name"] = GA
    item["issue_id"] = input()
    item['sth wrong'] = input()
    print(item)

    print()
    issule_info.append(item)
    JSONFIle_processing.write(issule_info, "issue_info.json")
    log.append(GA)
    JSONFIle_processing.write(log, 'issue_log.json')