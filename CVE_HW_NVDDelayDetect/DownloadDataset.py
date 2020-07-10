# -*- coding: utf-8 -*-

"""
Created on 2020-07-10 15:37  

@author: congyingxu
"""
import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from CommonFunction import MD5, File_processing, JSONFIle_processing
import time
import urllib.request

# need to modify
dataset_path = '../CVENVDDataset/'

cve_data_url = 'https://cve.mitre.org/data/downloads/allitems.xml'
nvd_data_url = 'https://nvd.nist.gov/feeds/json/cve/1.1/'
# 'https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-2017.json.gz'
# 'https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-2002.json.gz'


cve_md5_data = JSONFIle_processing.read(dataset_path + 'CVE/' + 'MD5.json')
nvd_md5_data = JSONFIle_processing.read(dataset_path + 'NVD/' + 'MD5.json')

def read():
    pass

def write():
    pass

def download():
    global cve_md5_data, nvd_md5_data
    local_time = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    print(local_time)

    # CVE
    print('CVE')
    # year = 2020
    # download
    print('downloading')
    register_path = dataset_path + 'CVE/' + 'allitems.xml'
    urllib.request.urlretrieve(cve_data_url, register_path)
    # check hash
    print('hashing')
    # register_file_hash = ''
    register_file_hash = MD5.md5sum_for_bigfile(register_path)
    lastest_year_hash = cve_md5_data['latest_hash']['2020']
    file_path = dataset_path + 'CVE/' + "allitems" + "__fdse__" + local_time + "__fdse__" + register_file_hash[:6] + ".xml"
    if lastest_year_hash == register_file_hash:  # 未变
        cve_md5_data['file_list']['2020'].append(file_path)
    else:  # 变了
        cve_md5_data['file_list']['2020'].append(file_path)
        cve_md5_data['diff_file_list']['2020'].append(file_path)
        cve_md5_data['latest_hash']['2020'] = register_file_hash

        # rename file
        dstFile = file_path
        srcFile = register_path
        File_processing.renameFile(srcFile, dstFile)


    # NVD
    print('NVD')
    for year in range(2002,2021):
        # download
        print(year)
        full_nvd_data_url = nvd_data_url + "nvdcve-1.1-" + str(year) + ".json.gz"
        print('downloading')
        register_path = dataset_path + 'NVD/' + 'nvd.json'
        urllib.request.urlretrieve(full_nvd_data_url, register_path)
        #check hash
        print('hashing')
        register_file_hash = MD5.md5sum_for_bigfile(register_path)
        lastest_year_hash = nvd_md5_data['latest_hash'][str(year)]
        file_path = dataset_path + 'NVD/' + "nvdcve-1.1-" + str(
            year) + "__fdse__" + local_time + "__fdse__" + register_file_hash[:6] + ".json.gz"  # 存储的name
        if lastest_year_hash == register_file_hash : #未变
            nvd_md5_data['file_list'][str(year)].append(file_path)
        else: #变了
            nvd_md5_data['file_list'][str(year)].append(file_path)
            nvd_md5_data['diff_file_list'][str(year)].append(file_path)
            nvd_md5_data['latest_hash'][str(year)] = register_file_hash

            # rename file
            dstFile = file_path
            srcFile = register_path
            File_processing.renameFile(srcFile, dstFile)

    JSONFIle_processing.write(cve_md5_data, dataset_path + 'CVE/' + 'MD5.json')
    JSONFIle_processing.write(nvd_md5_data, dataset_path + 'NVD/' + 'MD5.json')


def main():
    while 1:
        time.sleep(60 *60 * 6)
        download()
        # break

if __name__ == '__main__':
    # url = 'https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-2015.json.gz'
    # urllib.request.urlretrieve(url, 'nvdcve-1.1-2015.json.gz')
    main()