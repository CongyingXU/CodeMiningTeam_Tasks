# -*- coding: utf-8 -*-

"""
Created on 2020-05-01 09:50  

@author: congyingxu
"""
from CommonFunction import File_processing,JSONFIle_processing
import json

todo_dir = '/Users/congyingxu/Downloads/ShangqiTodo/'
lib_version_path = '/Users/congyingxu/Downloads/CodeMiningTeam_Tasks/SpecialCrawlingTask/Local_Data/lib_versions.json'

GA_path = 'Todo_GA_List0507.json'
todo_GA_num_list_path = 'Todo_GA_Num_List0507.json'
Todo_CMDorTask_path = 'Todo_CMDorTask_shangqi_0507.json'
GA = []
todo_GA_num_list = []

def generateTodoGA_list():
    global GA
    file_list = File_processing.walk_L1_FileNames(todo_dir)
    for file_name in file_list:
        if file_name.endswith('DS_Store'):
            continue
        # print(todo_dir + file_name)
        for ele in JSONFIle_processing.read(todo_dir + file_name):
            ga = ele['groupId'] + "__fdse__" + ele['artifactId']
            if ga not in GA:
                GA.append(ga)
            else:
                # print(ga)
                pass
    JSONFIle_processing.write(GA, GA_path)
    print(len(GA))  # 59

def generateTodoGANum_list():
    global GA, todo_GA_num_list

    lib_version = JSONFIle_processing.read(lib_version_path)
    for index in range(len( lib_version )):
        lib_str = lib_version[index]['lib']
        ga_str = lib_str.split('__fdse__')[0] + '__fdse__' + lib_str.split('__fdse__')[1]
        if ga_str in GA:
            todo_GA_num_list.append(index)

    JSONFIle_processing.write(todo_GA_num_list,todo_GA_num_list_path)

def generateFile():
    global GA, todo_GA_num_list

    task_content = {"Task_Todo": []}

    for ele in todo_GA_num_list:
        ele = int(ele)

        task_item = "/home/fdse/wangying/crawled_data/__fdse__/home/fdse/wangying/CrawlLibraries/data/" + "__fdse__" + str(
            ele) + "__fdse__" + str(ele + 1)
        task_content["Task_Todo"].append(task_item)

    with open(Todo_CMDorTask_path,'w') as f:
        f.write( json.dumps( task_content,indent=4 ) )




def main():
    global GA
    GA = JSONFIle_processing.read(GA_path)
    # generateTodoGA_list()
    generateTodoGANum_list()
    generateFile()

if __name__ == '__main__':
    main()

