#!/usr/bin/env python
# encoding: utf-8
"""

Created on 2020/1/7 19:25
@Author : CongyingXu

"""

from ImportLibraryJar import Config
from CommonFunction import JSONFIle_processing,File_processing
from ParseMaven import ParseMaven_LibraryListPage
from ParseMaven import ParseMaven_MetadataXML

LocalRepositoryPath = Config.LOCAL_REPOSITORY_PATH
ProcessedCrawledJarPath =  Config.PROCESSED_CRAWLEDJar_PATH
Crawled_liblis_path =  Config.CRAWLED_LIBRARY_LIST_PATH

Source = Config.SOURCE
Version = Config.VERSION
LibraryList_path = Config.PATH_LIBRARY_LIST
LibInfo_path = Config.PATH_LIB_INFO_PATH
Imported_Jar_log_path = Config.PATH_IMPORTING_JAR_LOG

lib_all_vN_path = Config.LOCAL_REPOSITORY_PATH + "data/lib_all_" + Config.VERSION + ".json"
maven_page_lib_name  = Config.MAVEN_PAGE_LIB_HTML
repo_page_lib_name = Config.REPO_PAGE_LIB_HTML
repo_url_name = Config.REPO_URL_TXT
maven_metadata_xml =  Config.MAVEN_METADATA_XML
version_all_vN_content_template = Config.TEMPLATE_VERSION_ALL_VN_JSON
version_all_vN_name = Config.VERSION_ALL_VN_JSON

maven_page_version_name  = Config.MAVEN_PAGE_VERSION_HTML
repo_page_version_name = Config.REPO_PAGE_VERSION_HTML
file_all_vN_content_template = Config.TEMPLATE_FILE_ALL_VN_JSON
file_all_vN_name = Config.FILE_ALL_VN_JSON

maven_repo_url_part = Config.URL_MAVEN_REPO_PART





LibraryList = []
LibInfo = {} # lib relative path in local repo;  folder_name

def getLiblistAndInfo():
    global LibraryList, LibInfo
    LibraryList_foldername_list = File_processing.walk_L1_Folders(ProcessedCrawledJarPath)
    LibraryList  = [ ele.split('__fdse__')[0] + "__fdse__" + ele.split('__fdse__')[1] for ele in LibraryList_foldername_list ]
    lib_all_vN = JSONFIle_processing.read(lib_all_vN_path)
    LibInfo_foldername = JSONFIle_processing.read(LibInfo_path)

    for lib in LibraryList:
        lib_all_vN[lib]["folder_name"] = LibInfo_foldername[lib]["GA_floder_name"]
    LibInfo = lib_all_vN

def getImportedGAList():
    with open(Imported_Jar_log_path,'r+') as f:
        content = f.read()
        Imported_GA_List = content.split('\n')
    return Imported_GA_List

# move to folder level 2: ../GA_md5(6)/xxx.html__fdse__vN
def move_L2_htmlFiles(lib_folder_name,target_path):
        maven_lib_html_path = ProcessedCrawledJarPath + lib_folder_name + '/' + maven_page_lib_name
        repo_lib_html_path = ProcessedCrawledJarPath + lib_folder_name + '/' + repo_page_lib_name
        repo_url_txt_path = ProcessedCrawledJarPath + lib_folder_name + '/' +  repo_url_name

        # print (maven_lib_html_path)
        # print (target_path + maven_page_lib_name + '__fdse__' + Version)
        File_processing.copyFile(maven_lib_html_path, target_path + maven_page_lib_name + '__fdse__' + Version)
        File_processing.copyFile(repo_lib_html_path, target_path + repo_page_lib_name + '__fdse__' + Version)
        File_processing.copyFile(repo_url_txt_path, target_path + repo_url_name + '__fdse__' + Version)
        # break

def parserRepoLibHTML(repo_lib_html_path):
    return ParseMaven_LibraryListPage.main(repo_lib_html_path)

def getLastupdateTime(metadata_xml_path):
    return ParseMaven_MetadataXML.main(metadata_xml_path)

# write level 2: ../GA_md5(6)/version_all_vN.json
def write_L2_version_all_vN(lib_folder_name,Crawled_GA_lib_path,Processed_GA_path,localRepo_GA_path,repo_lib_pagetime_dict):
    version_all_vN_content = version_all_vN_content_template

    # files:
    # 1 from processed path : folders
    folderlist = File_processing.walk_L1_Folders(Processed_GA_path)
    for foldername in folderlist:
        if len(foldername) >= 40:
            # print (repo_lib_pagetime_dict)
            # print (foldername)
            page_time = repo_lib_pagetime_dict[foldername[:44] + '...'] # handle exception,such as : v1.1.0-226-g847ecff2d8e26f249422247d7665fe15...
        else:
            page_time = repo_lib_pagetime_dict[foldername]
        item = { foldername:{"source":Source , "page_time": page_time} }
        version_all_vN_content["files"].update(item)
        # make dir

    # 2 from processed path : files
    filelist = File_processing.walk_L1_FileNames(Processed_GA_path)
    repo_url_path = Processed_GA_path + repo_url_name
    for filename in filelist:
        filename_path = Processed_GA_path + filename
        crawl_time = File_processing.getFileCreatedTime(filename_path)  # crawl time
        url_part = File_processing.read_TXTfile(repo_url_path)
        url_whole = maven_repo_url_part + url_part
        item = {filename: {Version: {"url": url_whole ,"crawl_time": crawl_time, "absolute_file_name": filename + "__fdse__" +Version}}}
        version_all_vN_content["files"].update(item)

    # 3 from downloaded LibList : files
    filelist = File_processing.walk_L1_FileNames(Crawled_GA_lib_path)
    for filename in filelist:
        if filename == "versions.json":
            continue
        page_time = repo_lib_pagetime_dict[filename]
        item = {filename: {Version: {"page_time": page_time, "absolute_file_name": filename + "__fdse__" +Version}}}
        version_all_vN_content["files"].update(item)

    # lastupdated
    try:
        metadata_xml_path = Crawled_liblis_path +lib_folder_name + '/' + maven_metadata_xml
        lastUpdated_time = getLastupdateTime(metadata_xml_path)
        if lastUpdated_time !='' :
            lastUpdated_time += "__fdse__" + Source
            version_all_vN_content["lastUpdated"].append(lastUpdated_time)
            print (Processed_GA_path)
            print (version_all_vN_content)
    except:
        # print ("Error: " + Processed_GA_path)
        pass

    # write version_all_vN.json
    version_all_vN_content_path = localRepo_GA_path + version_all_vN_name
    JSONFIle_processing.write(version_all_vN_content,version_all_vN_content_path)

# make director  level 2: ../GA_md5(6)/0.3-3/..
def make_L2_Versiondir(Processed_GA_path,target_path):
    folderlist = File_processing.walk_L1_Folders(Processed_GA_path)
    for foldername in folderlist:
        folder_path = target_path + foldername
        File_processing.creatFolder_IfExistPass(folder_path)
        target_GAV_folder_path = target_path + foldername + '/'
        Processed_GAV_path = Processed_GA_path + foldername + '/'

        # page time
        repo_version_html_path =Processed_GAV_path + repo_page_version_name
        repo_version_pagetime_info = parserRepoLibHTML(repo_version_html_path)["version/artifacts_info"]
        repo_version_pagetime_dict = {}
        for ele in repo_version_pagetime_info:
            repo_version_pagetime_dict[ele[0].strip('/')] = ele[1]

        # step 3 : files level: write and move files
        write_L3_file_all_vN(Processed_GAV_path,target_GAV_folder_path,Processed_GA_path,repo_version_pagetime_dict,foldername)
        move_L3_JarHtmlFiles(Processed_GAV_path,target_GAV_folder_path)
        print (target_GAV_folder_path)

# write level 3: ../GA_md5(6)/0.3-3/file_all_v1.json
def write_L3_file_all_vN(Processed_GAV_path,target_GAV_folder_path,Processed_GA_path,repo_version_pagetime_dict,GA_version):
    file_all_vN_content = file_all_vN_content_template

    filelist = File_processing.walk_L1_FileNames(Processed_GAV_path)
    repo_url_path = Processed_GA_path + repo_url_name
    for filename in filelist:
        if filename.endswith(".html"):
            filename_path = Processed_GAV_path + filename
            crawl_time = File_processing.getFileCreatedTime(filename_path)  # crawl time
            url_part = File_processing.read_TXTfile(repo_url_path)
            url_whole = maven_repo_url_part + url_part + GA_version
            item = {filename: {
                Version: {"url": url_whole, "crawl_time": crawl_time, "absolute_file_name": filename + "__fdse__" + Version}}}
        else:
            page_time = repo_version_pagetime_dict[filename]
            filename_path = Processed_GAV_path + filename
            crawl_time = File_processing.getFileCreatedTime(filename_path)  # crawl time
            item = {filename: {
                Version: { "crawl_time": crawl_time, "page_time": page_time, "absolute_file_name": filename + "__fdse__" + page_time}}}

        file_all_vN_content["files"].update(item)

    # write file_all_vN.json
    file_all_vN_content_path = target_GAV_folder_path + file_all_vN_name
    JSONFIle_processing.write(file_all_vN_content, file_all_vN_content_path)

# move to folder level 3: ../GA_md5(6)/xxx.html__fdse__vN Jar...
def move_L3_JarHtmlFiles(Processed_GAV_path,target_GAV_folder_path):
    filelist = File_processing.walk_L1_FileNames(Processed_GAV_path)
    for filename in filelist:
        filename_path = Processed_GAV_path + filename
        crawl_time = File_processing.getFileCreatedTime(filename_path)  # crawl time
        source_path = filename_path
        if filename.endswith(".html"):
            target_path = target_GAV_folder_path + filename + "__fdse__" +Version
        else:
            target_path = target_GAV_folder_path + filename + "__fdse__" + crawl_time.replace(':','-')
        File_processing.copyFile(source_path, target_path)

def main():
    getLiblistAndInfo()
    Imported_GA_List = getImportedGAList()

    for lib in LibraryList:
        if lib in Imported_GA_List:
            # print("Pass : " + filename)
            continue

        target_path = LocalRepositoryPath + LibInfo[lib]["path"]
        lib_folder_name = LibInfo[lib]["folder_name"]
        Processed_GA_path =   ProcessedCrawledJarPath + lib_folder_name + '/'
        Crawled_GA_lib_path = Crawled_liblis_path + lib_folder_name + '/'

        repo_lib_html_path = ProcessedCrawledJarPath + lib_folder_name + '/' + repo_page_lib_name
        repo_lib_pagetime_info = parserRepoLibHTML(repo_lib_html_path)["version/artifacts_info"]
        repo_lib_pagetime_dict = {}
        for ele in repo_lib_pagetime_info:
            repo_lib_pagetime_dict[ele[0].strip('/')] = ele[1]

        # main course:
        # step 1: version level, not time-consuming
        move_L2_htmlFiles(lib_folder_name,target_path)
        write_L2_version_all_vN(lib_folder_name,Crawled_GA_lib_path,Processed_GA_path,target_path,repo_lib_pagetime_dict)
        # step 2: files level, make dir and handle file level
        make_L2_Versiondir(Processed_GA_path, target_path)
        print (target_path)

        Imported_GA_List.append(lib)
        with open(Imported_Jar_log_path, 'a+') as f:
            f.write(lib + '\n')
        break

if __name__ == '__main__':
    main()






