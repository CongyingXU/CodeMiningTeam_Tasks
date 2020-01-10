#!/usr/bin/env python
# encoding: utf-8
"""

Created on 2020/1/7 10:45
@Author : CongyingXu

functions: Import library list to local repository

"""

from CommonFunction import File_processing,JSONFIle_processing,MD5
from ImportLibraryJar import Config
import os

class CrawledLibraryList:
    # # Meta.json
    # Version = "v1"
    # Time = "2019-10-15-2019-11-15"
    # Source  = "Central: https://repo1.maven.org/maven2/"
    # LibRangeIsAll = True
    #
    # # lib_all_vN.json
    # LocalRepositoryPath = "F:/Jar/"
    # CrawledLibraryListPath = "F:/Downloads/Downloads_LibList/v1_191015_rangeALL/"

    # Meta.json
    Version = Config.VERSION
    Time = Config.TIME
    Source = Config.SOURCE
    LibRangeIsAll = Config.LIB_RANGE_IS_ALL

    # lib_all_vN.json
    LocalRepositoryPath = Config.LOCAL_REPOSITORY_PATH
    CrawledLibraryListPath = Config.CRAWLED_LIBRARY_LIST_PATH


    def __init__(self):
        self.getLibraryList()

    def getLibraryList(self):
        LibraryListFilePath = "TemporaryData/" + self.Version +"LibList.json"
        LibrariesInfoPath = "TemporaryData/" + self.Version + "LibInfo.json"
        if os.path.exists( LibraryListFilePath ) and os.path.exists( LibrariesInfoPath ):
            print( "_____________________________")
            print( "Reading Library List&Info File ..." )
            self.LibraryList = JSONFIle_processing.read(LibraryListFilePath)
            self.LibInfo = JSONFIle_processing.read(LibrariesInfoPath)
        else:
            print( "_____________________________")
            print( "Writing Library List&Info File ...")
            CrawledLibraryList_md5 = File_processing.walk_L1_Folders(self.CrawledLibraryListPath)
            self.LibraryList = [ ele.split("__fdse__")[0] + "__fdse__" + ele.split("__fdse__")[1] for ele in CrawledLibraryList_md5]
            self.LibInfo = {  }
            for ele in CrawledLibraryList_md5:
                lib_GA = ele.split("__fdse__")[0] + "__fdse__" + ele.split("__fdse__")[1]
                self.LibInfo[lib_GA] = {'GA_folder_name': ele}

            JSONFIle_processing.write(self.LibraryList, LibraryListFilePath)
            JSONFIle_processing.write(self.LibInfo, LibrariesInfoPath)



CrawledLibList_obj = CrawledLibraryList()
Meta_path = CrawledLibList_obj.LocalRepositoryPath + "data/meta.json"
lib_all_vN_path = CrawledLibList_obj.LocalRepositoryPath + "data/lib_all_" + CrawledLibList_obj.Version + ".json"
LogPath = Config.PATH_IMPORTING_LIB_LIST_LOG

FinishedImportedLib_list = []



# write folder level 1: lib_all_v1.json
def append_L1_Meta():
    Meta_content = JSONFIle_processing.read(Meta_path)
    new_Meta_item = {CrawledLibList_obj.Version:{"time":CrawledLibList_obj.Time, "source":CrawledLibList_obj.Source}}
    Meta_content["crawl_dir_time"].update( new_Meta_item )
    new_Meta_item_isall =  {CrawledLibList_obj.Version:{"is_all":CrawledLibList_obj.LibRangeIsAll}}
    Meta_content["lib_all"].update( new_Meta_item_isall )
    JSONFIle_processing.write(Meta_content,Meta_path)


# make director /aaa/....
def make_L1_Libdir():
    for GA in CrawledLibList_obj.LibraryList:
        # make folder /aaa/...
        folder_name = GA[:2]
        folder_path = CrawledLibList_obj.LocalRepositoryPath + "data/libraries/" + folder_name + '/'
        if os.path.exists(folder_path):
            pass
        else: # /aa/..不存在时
            try:
                os.mkdir(folder_path)
            except:
                print("Exception: mkdir folder_path" + folder_path , GA)
                folder_name = "default"
                folder_path = CrawledLibList_obj.LocalRepositoryPath + "data/libraries/" + folder_name + '/'
                os.mkdir(folder_path)
                break

        # make folder /GA_MD5(6)
        CrawledGA_path = CrawledLibList_obj.CrawledLibraryListPath + GA + '/'
        GA_folder_name = CrawledLibList_obj.LibInfo[GA]["GA_folder_name"]
        LocalRepoGA_path = folder_path + GA_folder_name + "/"
        CrawledLibList_obj.LibInfo[GA]["LocalRepoGA_relative_path"] = "data/libraries/"+folder_name +"/"+ GA_folder_name +'/'

        if os.path.exists(LocalRepoGA_path):
            print("Existing: mkdir LocalRepoGA_path " + LocalRepoGA_path)
            pass
        else:
            try:
                os.mkdir(LocalRepoGA_path)
            except:
                print("Exception: mkdir LocalRepoGA_path " + LocalRepoGA_path)
                break


# write folder level 1: lib_all_v1.json
def write_L1_liballvN():
    print('xxxxx')
    lib_all_vN_content = {}
    print(lib_all_vN_path)
    for GA in CrawledLibList_obj.LibraryList:
        lib_all_vN_content[GA] = {"path":CrawledLibList_obj.LibInfo[GA]["LocalRepoGA_relative_path"]}

    JSONFIle_processing.write(lib_all_vN_content,lib_all_vN_path)


# move to folder level 2: ../GA_md5(6)/metadata.xml__fdse__vN
def move_L2_matadataFiles():
    global FinishedUntarFilesList
    with open(LogPath, 'r+') as f:
        content = f.read()
        FinishedImportedLib_list = content.split('\n')


    for GA in CrawledLibList_obj.LibraryList:
        for GA in FinishedImportedLib_list:
            if GA in FinishedUntarFilesList:
                # print("Pass : " + filename)
                continue

        print(GA)
        GA_folder_name = CrawledLibList_obj.LibInfo[GA]["GA_folder_name"]
        Crawled_GA_floder_path = CrawledLibList_obj.CrawledLibraryListPath + GA_folder_name

        files_list = File_processing.walk_L1_FileNames(Crawled_GA_floder_path)
        lib_all_vN_content = JSONFIle_processing.read(lib_all_vN_path)
        target = CrawledLibList_obj.LocalRepositoryPath + lib_all_vN_content[GA]["path"]

        for filename in files_list:
            source = Crawled_GA_floder_path + '/' + filename
            File_processing.copyFile(source,target + filename+'__fdse__'+CrawledLibList_obj.Version)
            # print(source, target + filename+'__fdse__'+CrawledLibList_obj.Version)

        # register
        FinishedImportedLib_list.append(GA)
        with open(LogPath, 'a+') as f:
            f.write(GA + '\n')
        f.close()

def main():
    # step1: append meta.json and lib_all_vN.json
    if not os.path.exists(lib_all_vN_path):
        append_L1_Meta()
        make_L1_Libdir()
        write_L1_liballvN()

    # step2: move and rename files
    move_L2_matadataFiles()


if __name__ == '__main__':
    main()





