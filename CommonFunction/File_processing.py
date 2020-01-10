#!/usr/bin/env python
# encoding: utf-8
"""

Created on 2019/10/16 12:27
@Author : CongyingXu

用于进行文件相关操作
"""
import os,sys
import os.path
import shutil
import tarfile
import time

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

# rootdir -> list: all Folders in Level 1
def walk_L1_Folders(rootdir):
    for parent, dirnames, filenames in os.walk(rootdir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字

        return dirnames

# rootdir -> list: all filenames in Level 1
def walk_L1_FileNames(rootdir):
    for parent, dirnames, filenames in os.walk(rootdir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字

        return filenames



def creatFileFolder(path):
    # if os.path.exists(path):
    #     shutil.rmtree(path)
    return os.mkdir(path)

def creatFolder_IfExistPass(path):
    if os.path.exists(path):
        return -1
    else:
        return os.mkdir(path)

def creatFolder_IfExistRM(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    return os.mkdir(path)


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

def copyFile(source,target):
    # source = 'current/test/test.py'
    # target = '/prod/new'

    # # assert not os.path.isabs(source)
    # target = os.path.join(target, os.path.dirname(source))

    # # create the folders if not already exists
    # os.makedirs(target)

    # adding exception handling
    try:
        shutil.copy(source, target)
    except IOError as e:
        print("Unable to copy file. %s" % e)
    except:
        print("Unexpected error:", sys.exc_info())
        
def copyFolder(source_path,target_path):
    try:
        shutil.copytree(source_path, target_path)
        return 0
    except IOError as e:
        # print("Unable to copy file. %s" % e)
        pass
    except:
        print("Unexpected error:", sys.exc_info())
    return -1

def copyFolder_deleteOld(source_path,target_path):
    if os.path.exists(target_path):
        deleteFolder(target_path)

    copyFolder(source_path,target_path)


def deleteFolder(dir):
    shutil.rmtree(dir, True)  # 最后删除img总文件夹


import tarfile
def untarFile(fname, dirs):
    tar = tarfile.open(fname)
    names = tar.getnames()
    for name in names:
        try:
            tar.extract(name, path=dirs)
        except Exception as e:
            # print(e)
            pass

    tar.close()


def read_TXTfile(path):
    with open(path,'r') as f :
        content = f.read()
        return content

# https://blog.csdn.net/Areigninhell/article/details/86519077
def getFileSize(filepath):
    size = os.path.getsize(filepath)
    return size

# https://blog.csdn.net/thomaswu1992/article/details/90477482
def TimeStampToTime(timestamp):
    timeStruct = time.localtime( timestamp)
    return time.strftime( '%Y-%m-%d %H:%M:%S', timeStruct )

def getFileCreatedTime(filepath):
    t = os.path.getmtime(filepath)
    return TimeStampToTime(t)

def getFolderSize(folderpath):
    size=0
    for root, dirs, files in os.walk(folderpath):
        for f in files:
            size += os.path.getsize(os.path.join(root, f))
    return size



if __name__ == '__main__':
    walk_FileDir('e:/libs')
    # creatFileFolder('e:/Jars-MD5/AAA/')