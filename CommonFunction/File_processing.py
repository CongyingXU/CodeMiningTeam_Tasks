#!/usr/bin/env python
# encoding: utf-8
"""

Created on 2019/10/16 12:27
@Author : CongyingXu

用于进行文件相关操作
"""
import os
import os.path
import shutil

# rootdir -> list: all file full name
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



def creatFileFolder(path):
    # if os.path.exists(path):
    #     shutil.rmtree(path)
    os.mkdir(path)

def moveFile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
            print( "%s not exist!" % (srcfile))
            return ( "%s not exist!" % (srcfile) +'\n')
    elif os.path.exists(dstfile): #文件已存在
        print(dstfile+" exists, from " + srcfile)
        return (dstfile+" exists, from " + srcfile +'\n')
    else:
            fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
            if not os.path.exists(fpath):
                os.makedirs(fpath)  # 创建路径
            shutil.move(srcfile, dstfile)  # 移动文件
            # print("move %s -> %s " % (srcfile, dstfile))
            return ("move %s -> %s " % (srcfile, dstfile)+'\n')



if __name__ == '__main__':
    walk_FileDir('e:/libs')
    # creatFileFolder('e:/Jars-MD5/AAA/')