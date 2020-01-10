#!/usr/bin/env python
# encoding: utf-8
"""

Created on 2020/1/7 19:46
@Author : CongyingXu

"""
###################################################
# Meta.json
VERSION = "v1"
TIME = "2019-10-15-2019-11-15"
SOURCE  = "Central: https://repo1.maven.org/maven2/"
LIB_RANGE_IS_ALL = True


###################################################
# path
# path of local Jar repo stored in Server
LOCAL_REPOSITORY_PATH = "F:/Jar/"
# path of crawled LibList and Jars
CRAWLED_LIBRARY_LIST_PATH = "F:/Downloads/Downloads_LibList/v1_191015_rangeALL/"
CRAWLED_Jar_PATH = "F:/Downloads/Downloads_Jar/CrawledJars_v1_191213/"
# path of pre-precessed crawled Jar.zip
PROCESSED_CRAWLEDJar_PATH  = "F:/Processed_Downloads_Jars/CrawledJars_v1_191213/"




###################################################
# fixed path
# path of log
PATH_IMPORTING_LIB_LIST_LOG = "TemporaryData/" + VERSION + "ImportingLibList.log"
PATH_PROCESSING_CRAWLED_JAR_LOG = "TemporaryData/" + VERSION + "ProcessingCrawledJar.log"
PATH_IMPORTING_JAR_LOG = "TemporaryData/" + VERSION + "ImportingProcessedJar.log"
PATH_LIBRARY_LIST = "TemporaryData/" + VERSION + "LibList.json"
PATH_LIB_INFO_PATH = "TemporaryData/" + VERSION + "LibInfo.json"





###################################################
# filename
# libList
MAVEN_PAGE_LIB_HTML = "maven-page-lib.html"
REPO_URL_TXT = "repo_url.txt"
REPO_PAGE_LIB_HTML = "repo-page-lib.html"
MAVEN_METADATA_XML = "maven-metadata.xml"
VERSION_ALL_VN_JSON = "version_all_" + VERSION + ".json"
# versionList
MAVEN_PAGE_VERSION_HTML = "maven-page-version.html"
REPO_PAGE_VERSION_HTML = "repo-page-version.html"
FILE_ALL_VN_JSON = "file_all_" + VERSION + ".json"


###################################################
# data structure template
TEMPLATE_VERSION_ALL_VN_JSON = { "files":{} , "lastUpdated":[] }
TEMPLATE_FILE_ALL_VN_JSON = { "files":{} }


###################################################
# varibles
# url
URL_MAVEN_REPO_PART = "https://repo1.maven.org/maven2/"