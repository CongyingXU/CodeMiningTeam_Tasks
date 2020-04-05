# -*- coding: utf-8 -*-

"""
Created on 2020-04-04 13:57  

@author: congyingxu
"""

from CommonFunction import JSONFIle_processing

NVDDataset_dir = "/Users/congyingxu/Downloads/CVE/DataSet-NVD/"
NVDYearDataset = {}
NVD_CVEID_list_path = "/Users/congyingxu/Downloads/CVE/MetaData/NVD_CVEID_list.json"
NVD_CVEID_list = JSONFIle_processing.read(NVD_CVEID_list_path)


NVDItems_dir = "/Users/congyingxu/Downloads/CVE/DataSet-NVD/NVDItems/"
def separateCVEItems():
    for year in range(2002,2021):
        file_path = NVDDataset_dir + "nvdcve-1.1-" + str(year) +'.json'
        year_dataset_content = JSONFIle_processing.read(file_path)

        # separate:
        CVE_Items = year_dataset_content['CVE_Items']
        for CVE_Item in CVE_Items:
            CVEID = CVE_Item['cve']['CVE_data_meta']['ID']
            print(CVEID)
            path = NVDItems_dir + CVEID +'.json'
            JSONFIle_processing.write(json_content=CVE_Item, path=path)
            # break
if __name__ == '__main__':
    separateCVEItems()

