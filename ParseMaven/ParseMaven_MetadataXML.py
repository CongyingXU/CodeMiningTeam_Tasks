#!/usr/bin/env python
# encoding: utf-8
"""

Created on 2020/1/8 15:52
@Author : CongyingXu

"""

from bs4 import BeautifulSoup

def read(xml_path):
    with open(xml_path,'r') as f:
        return f.read()

def bs4_paraser(xml):
    soup = BeautifulSoup(xml, 'html.parser')
    try:
        lastUpdated = soup.find_all('lastUpdated', limit=1)[0]
        lastUpdated_time = lastUpdated.get_text()
    except:
        lastUpdated_time = ''
    # print("lastUpdated_time: "+lastUpdated_time)
    return lastUpdated_time


def main(xml_path):
    xml = read(xml_path)
    lastUpdated_time = bs4_paraser(xml)
    return lastUpdated_time

if __name__ == '__main__':
    xml_path = 'LibraryListPage_test.html'
    print( main(xml_path) )

