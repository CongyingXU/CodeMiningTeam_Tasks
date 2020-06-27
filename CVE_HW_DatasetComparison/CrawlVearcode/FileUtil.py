# -*- coding: utf-8 -*-

"""
Created on 2020-03-27 01:22  

@author: congyingxu
"""

import hashlib
import json

import ijson

def read_json(path):
    # print("rrrrrrrrrrrrrrrrrrr start read json")
    try:
        with open(path, encoding='utf-8') as json_file:
            data = json.load(json_file)
            # print("rrrrrrrrrrrrrrrrrrr finish read json")
            return data
    except Exception as e:
        with open(path, encoding='gbk') as json_file:
            data = json.load(json_file)
            # print("rrrrrrrrrrrrrrrrrrr finish read json")
            return data

def read_json_list_part(path, start, end):
    print("rrrrrrrrrrrrrrrrrrr start read json part")
    try:
        with open(path, encoding='utf-8') as json_file:
            data = ijson.items(json_file, 'item')
            new_data = []
            index = 0
            for e in data:
                if index >= start and index < end:
                    new_data.append(e)
                index += 1
                if index > end:
                    break
            print("rrrrrrrrrrrrrrrrrrr finish read json part")
            return new_data
    except Exception as e:
        with open(path, encoding='gbk') as json_file:
            data = ijson.items(json_file, 'item')
            new_data = []
            index = 0
            for e in data:
                if index >= start and index < end:
                    new_data.append(e)
                index += 1
                if index > end:
                    break
            print("rrrrrrrrrrrrrrrrrrr finish read json part")
            return new_data

def write_json(path,json_data):
    with open(path, 'w', encoding='utf-8') as file_object:
        json.dump(json_data, file_object)

def write_json_format(path,json_data):
    with open(path, 'w', encoding='utf-8') as file_object:
        json.dump(json_data, file_object, indent=4)

def read_file_lines(path):
    try:
        with open(path, "r", encoding='utf-8') as f:
            lines = f.readlines()
            for i in range(len(lines)):
                lines[i] = lines[i].strip('\n')
        return lines
    except Exception as e:
        with open(path, "r", encoding='gbk') as f:
            lines = f.readlines()
            for i in range(len(lines)):
                lines[i] = lines[i].strip('\n')
        return lines

def read_file_string(path):
    with open(path, "r", encoding='utf-8') as f:
        content = f.read()
    return content

def read_file_content(path):
    with open(path, "rb") as f:
        content = f.read()
    return content

def write_file(file_path,content):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    f.close()

def append_file(file_path,content):
    with open(file_path, "a", encoding='utf-8') as f:
        f.write(content + "\n")
    f.close()

def md5sum(file_path):
    md5obj = hashlib.md5()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(2024)
            if not data:
                break
            md5obj.update(data)  # update添加时会进行计算
    _hash = md5obj.hexdigest()
    return str(_hash)


def str2md5(string):
    md5obj = hashlib.md5()
    md5obj.update(string.encode("utf8"))
    _hash = md5obj.hexdigest()
    return str(_hash)
