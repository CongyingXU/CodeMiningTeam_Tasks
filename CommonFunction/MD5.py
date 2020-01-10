#!/usr/bin/env python
# encoding: utf-8
"""

Created on 2019/10/16 13:13
@Author : CongyingXu

用于生成MD5相关操作
"""
import hashlib

# from 颖姐, 已验证：maven jar包MD5码一致
# file->md5
def md5sum(file_path):
    with open(file_path, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        _hash = md5obj.hexdigest()
    return str(_hash)

def MakeMD5byString(str_content):
    md5obj = hashlib.md5()
    md5obj.update(str_content.encode('utf-8'))
    _hash = md5obj.hexdigest()
    return str(_hash)


# print(md5sum('c:/Users/Congy/Downloads/junit-4.8.1.jar'))