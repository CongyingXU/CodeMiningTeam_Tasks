# -*- coding: utf-8 -*-

"""
Created on 2019-12-02 18:40  

@author: congyingxu

sample :
1、https://repo1.maven.org/maven2/junit/junit/
2、https://repo1.maven.org/maven2/junit/junit/3.8/
"""

from bs4 import BeautifulSoup

def read():
    with open('LibraryListPage_test.html','r') as f:
    # with open('ArtifactsListPage_test.html', 'r') as f:
        return f.read()

def bs4_paraser(html):

    data_dict = {}
    library = ''
    version = ''
    time = ''

    soup = BeautifulSoup(html, 'html.parser')
    header = soup.find_all('header', limit=1)
    library = header[0].find('h1').string
    data_dict['library/artifact'] = library
    data_dict['version/artifacts_info'] = []

    pre = soup.find_all('pre', attrs={'id': 'contents'}, limit=1)[0]
    a_  = pre.find_all('a')
    # print(a_)
    # print(pre.get_text().split('\n'))

    for ele in pre.get_text().split('\n')[1:]:
        # print(ele)
        value_list = ele.split()
        if len(value_list)>0:
            if value_list[0] == '../':
                pass
            else:
                version = value_list[0]
                time = value_list[1]+' '+value_list[2]
                data_dict['version/artifacts_info'].append( (version,time) )

    return data_dict




def main():
    html = read()
    data_dict = bs4_paraser(html)
    print(data_dict)

if __name__ == '__main__':
    main()

