# -*- coding: utf-8 -*-

"""
Created on 2020-02-06 12:17  

@author: congyingxu
"""

from bs4 import BeautifulSoup
import json

dictionary_file_path = "LocalData/official-cpe-dictionary_v2.3.xml"
cpe_reference_data_file_path = "LocalData/CPE_references.json"
cpe_VPListdata_file_path = "LocalData/CPE_VP.json"

class ProcessCPEDictionnary:

    DICTIONARY_PATH = dictionary_file_path
    CPE_REFERENCE_DATA_FILE_PATH = cpe_reference_data_file_path
    CPE_VP_DATA_FILE_PATH = cpe_VPListdata_file_path

    CPE_PEODUCT_SET = set()
    CPE_REFERENCE_TYPE_SET = set()
    CPE_REFERENCE_DATA = {"reference_type":[] , "VP_references":{}}

    def read(self):
        with open(self.DICTIONARY_PATH,'r') as f:
            xml_content = f.read()
        return xml_content

    def read_reference_data(self):
        with open(self.CPE_REFERENCE_DATA_FILE_PATH,'r') as f:
            json_content = json.loads( f.read() )
            self.CPE_REFERENCE_DATA = json_content
        return json_content


    def process(self, xml_content):
        soup = BeautifulSoup(xml_content, 'html.parser')
        cpe_list = soup.find_all('cpe-item')
        for cpe_ele in cpe_list:

            cpe_23 = cpe_ele.find_all('cpe-23:cpe23-item')[0]
            cpe_23_name = cpe_23.get("name")
            VP = cpe_23_name.split(':')[3] + "__fdse__" + cpe_23_name.split(':')[4]
            # print(cpe_23)
            # print(cpe_23.get("name"))
            # print(VP)
            # break
            self.CPE_PEODUCT_SET.add(VP)


            references = cpe_ele.find_all("reference")
            if len(references) > 0:
                for ref_ele in references:
                    reference_type = ref_ele.get_text()
                    reference_url = ref_ele.get("href")
                    # print(references)
                    # print(reference_type)
                    # print(reference_url)


                    self.CPE_REFERENCE_TYPE_SET.add(reference_type)
                    if VP in self.CPE_REFERENCE_DATA["VP_references"].keys():
                        if reference_type in self.CPE_REFERENCE_DATA["VP_references"][VP].keys():
                            self.CPE_REFERENCE_DATA["VP_references"][VP][reference_type].add(reference_url)
                        else:
                            self.CPE_REFERENCE_DATA["VP_references"][VP][reference_type] = set()
                            self.CPE_REFERENCE_DATA["VP_references"][VP][reference_type].add(reference_url)
                    else:
                        self.CPE_REFERENCE_DATA["VP_references"][VP] = {reference_type:set()}
                        self.CPE_REFERENCE_DATA["VP_references"][VP][reference_type].add(reference_url)






        print(self.CPE_REFERENCE_DATA)
        print(self.CPE_PEODUCT_SET)
        print(self.CPE_REFERENCE_TYPE_SET)


        self.CPE_REFERENCE_DATA["reference_type"] = list(self.CPE_REFERENCE_TYPE_SET)
        for VP_ele in self.CPE_REFERENCE_DATA["VP_references"].keys():
            for reference_type_ele in self.CPE_REFERENCE_DATA["VP_references"][VP_ele].keys():
                self.CPE_REFERENCE_DATA["VP_references"][VP_ele][reference_type_ele] = list( self.CPE_REFERENCE_DATA["VP_references"][VP_ele][reference_type_ele])


    def write(self):
        with open(self.CPE_REFERENCE_DATA_FILE_PATH,'w') as f:
            f.write( json.dumps(self.CPE_REFERENCE_DATA, indent = 4) )

        with open(self.CPE_VP_DATA_FILE_PATH, 'w') as f:
            f.write(json.dumps( list(self.CPE_PEODUCT_SET) , indent=4))
            print("(20200612) CPE product len:", len(self.CPE_PEODUCT_SET))




    def main(self):
        xml_content = self.read()
        print('reading over!')
        self.process(xml_content)
        self.write()

if __name__ == '__main__':
    ProcessCPEDictionnary().main()