#!/usr/bin/env python
# encoding: utf-8
"""

Created on 2020/1/7 20:08
@Author : CongyingXu

founctions:
1 pre-process crawled Jars , move and unzip
"""
from ImportLibraryJar import Config
from CommonFunction import File_processing
import os
import json


CrawledJarsPath = Config.CRAWLED_Jar_PATH
ProcessedCrawledJarPath =  Config.PROCESSED_CRAWLEDJar_PATH
LogPath = Config.PATH_PROCESSING_CRAWLED_JAR_LOG
LibVersionpath = Config.PATH_LIB_VERSION

TarFilesList = []
FinishedUntarFilesList = []
Lib_Version_data = []

def init():
    global Lib_Version_data,LibVersionpath
    with open(LibVersionpath, 'r') as f:
        Lib_Version_data = json.loads(f.read())


def getZIPfileslist():
    global ZipFilesList
    crawled_files_list = File_processing.walk_L1_FileNames(CrawledJarsPath)
    for filename in crawled_files_list:
        if filename.endswith("tar.gz"):
            task_num = filename.split("CompletedTask")[1].split('_')[0]
            start_num = task_num.split('-')[0]
            end_num = task_num.split('-')[1]
            if start_num != end_num:
                TarFilesList.append(filename)

def getSuccessfulCrawledGAlist(log_path):
    with open(log_path,'r') as f:
        log_content = f.read()

    log_lines = log_content.split('\n')
    successful_GA_num = []
    for log_line in log_lines:
        if len(log_line) == 0:
            continue
        if len( log_line.split("__fdse__") ) == 1:
            successful_GA_num.append( int(log_line) )
    # print(successful_GA_num)
    successful_GA = []
    for num_ele in successful_GA_num:
        GA_ = Lib_Version_data[num_ele]["lib"]
        # print(num_ele,GA_)
        successful_GA.append(GA_)

    return successful_GA


def UntarCopyDelete_crawledFiles():
    global FinishedUntarFilesList
    with open(LogPath,'r+') as f:
        content = f.read()
        FinishedUntarFilesList = content.split('\n')

    for filename in TarFilesList:
        if filename in FinishedUntarFilesList:
            # print("Pass : " + filename)
            continue

        # Untar
        print(TarFilesList.index(filename), len(TarFilesList),"Untar : "+ filename)
        filepath = CrawledJarsPath + filename
        File_processing.untarFile(filepath,CrawledJarsPath)

        # Copy
        source_folder_parent_path = CrawledJarsPath + "home/fdse/wangying/crawled_data/lib/"
        source_folder_log_path = CrawledJarsPath + "home/fdse/wangying/crawled_data/log.txt"
        # for XCY mac debug
        # source_folder_parent_path = "/Users/congyingxu/Downloads/" + "home/fdse/wangying/crawled_data/lib/"
        # source_folder_log_path = "/Users/congyingxu/Downloads/" + "home/fdse/wangying/crawled_data/log.txt"
        successful_crawled_GAs = getSuccessfulCrawledGAlist(source_folder_log_path)
        source_folder_list = File_processing.walk_L1_Folders(source_folder_parent_path)
        target = ProcessedCrawledJarPath

        for source_folder in source_folder_list:
            # print(successful_crawled_GAs)
            # print(source_folder)
            # print(source_folder_list)
            if source_folder not in successful_crawled_GAs:
                print("Unsuccessful Crawled GA: ", source_folder)
                continue

            source_folder_path = source_folder_parent_path + source_folder +'/'
            target_path = target + source_folder +'/'

            # copy result
            copy_result = File_processing.copyFolder(source_folder_path, target_path)
            # unsuccessful copy?
            if copy_result == -1:
                # whether the target_path existing?
                if os.path.exists(target_path):
                    # new one > the old
                    # print(File_processing.getFolderSize(source_folder_path))
                    # print(File_processing.getFolderSize(target_path))
                    if File_processing.getFolderSize(source_folder_path) > File_processing.getFolderSize(target_path):
                        File_processing.copyFolder_deleteOld(source_folder_path, target_path)
                        print("Overwrite : " + source_folder_path)
                        print("Overwrite : " + filename)

        # Delete
        File_processing.deleteFolder(CrawledJarsPath + "home/")

        # register
        FinishedUntarFilesList.append(filename)
        with open(LogPath, 'a+') as f:
            f.write(filename + '\n')
        f.close()
# crawled_data_code-mining109_CompletedTask33-49_2019_12_19_14_35_08.tar.gz


def main():
        init()
        getZIPfileslist()
        UntarCopyDelete_crawledFiles()

if __name__ == '__main__':
    main()
