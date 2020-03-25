# -*- coding: utf-8 -*-

"""
Created on 2020-02-17 00:54  

@author: congyingxu
"""

import json

VP_POMfile_data = {}

def read():
    for i in [1,2,3]:
        file_path = "Local_Data/VP_Git_POMFile" + str(i) + ".json"
        with open(file_path,'r') as f:
            content = json.loads( f.read() )

        for VP in content.keys():
            if len( content[VP] )==0 :
                continue
            else:
                VP_POMfile_data[VP] = content[VP]


# def collect():
#     for VP in VP_POMfile_data.keys():
#         if len( VP_POMfile_data[VP] )==0 :
#             VP_POMfile_data.pop(VP)


def write():
    print( "VP_POMfile_data" ,len(VP_POMfile_data.keys()) )
    file_path = "Local_Data/VP_Git_POMFile.json"
    with open(file_path, 'w') as f:
        f.write( json.dumps( VP_POMfile_data,indent=4 ) )
        # content = json.loads(f.read())

read()
# collect()
write()
