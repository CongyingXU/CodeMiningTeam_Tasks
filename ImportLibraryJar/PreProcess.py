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



CrawledJarsPath = Config.CRAWLED_Jar_PATH
ProcessedCrawledJarPath =  Config.PROCESSED_CRAWLEDJar_PATH
LogPath = Config.PATH_PROCESSING_CRAWLED_JAR_LOG

TarFilesList = []
FinishedUntarFilesList = []

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

def UntarCopyDelete_crawledFiles():
    global FinishedUntarFilesList
    with open(LogPath,'r') as f:
        content = f.read()
        FinishedUntarFilesList = content.split('\n')

    for filename in TarFilesList:
        if filename in FinishedUntarFilesList:
            # print("Pass : " + filename)
            continue

        # Untar
        # print("Untar : "+ filename)
        filepath = CrawledJarsPath + filename
        File_processing.untarFile(filepath,CrawledJarsPath)

        # Copy
        source_folder_parent_path = CrawledJarsPath + "home/fdse/wangying/crawled_data/lib/"
        source_folder_list = File_processing.walk_L1_Folders(source_folder_parent_path)
        target = ProcessedCrawledJarPath
        for source_folder in source_folder_list:
            source_folder_path = source_folder_parent_path + source_folder +'/'
            target_path = target + source_folder +'/'
            # unsuccessful copy?
            if File_processing.copyFolder(source_folder_path, target_path) == -1:
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
    getZIPfileslist()
    UntarCopyDelete_crawledFiles()

if __name__ == '__main__':
    main()
