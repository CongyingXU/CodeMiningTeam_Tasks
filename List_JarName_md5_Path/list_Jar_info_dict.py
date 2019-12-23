# -*- coding: utf-8 -*-

"""
Created on 2019-12-03 16:11  

@author: congyingxu
"""
import os,json

def walk_FileDir(rootdir):
    #rootdir = "d:/code/su/data"  # 指明被遍历的文件夹
    file_list = []
    #dfs
    for parent, dirnames, filenames in os.walk(rootdir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        # for dirname in dirnames:  # 输出文件夹信息
        #     print ("parent is:" + parent)
        #     print("dirname is" + dirname)

        for filename in filenames:  # 输出文件信息
            full_name = os.path.join(parent, filename)
            file_list.append(full_name)
        #     print("parent is:" + parent)
        #     print("filename is:" + filename)
        #     print("the full name of the file is:" + os.path.join(parent, filename) ) # 输出文件路径信息
    return file_list

def main():

    data_dict={}

    file_list = walk_FileDir('/Volumes/Samsung_T5/Jars-MD5')
    for file_path in file_list:
        if file_path.endswith('.md5'):
            with open(file_path,'r') as f:
                md5 = f.read()

            jar_name = file_path.split('/')[-1][:-4]
            path = file_path.split('/Volumes/Samsung_T5/')[1].split(jar_name)[0]

            data_dict[jar_name] = {}
            data_dict[jar_name]['md5'] = md5
            data_dict[jar_name]['path'] = path


    with open('Jar-MD5.json','w') as f:
        f.write( json.dumps( data_dict,indent=4 ) )
    print(len(data_dict))



if __name__ == '__main__':
    main()