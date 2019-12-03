# -*- coding: utf-8 -*-

"""
Created on 2019-12-02 21:06  

@author: congyingxu

https://mvnrepository.com/artifact/junit/junit
"""


from bs4 import BeautifulSoup

def read():
    with open('LibraryHomepage_test.html','r') as f:
    # with open('ArtifactsListPage_test.html', 'r') as f:
        return f.read()

def bs4_paraser(html):

    data_dict = {}
    library = ''
    version = ''
    time = ''

    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find_all('div', attrs={'id': 'maincontent'})[0]
    table = div.find('table', attrs={'class': 'grid'})
    for tr in table.find_all('tr'):
        # print(tr)
        th = tr.find_all('th')[0].string
        # td = tr.find_all('td')[0].get_text()
        # print(th,td)
        # print()

        if th == 'License':
            License_info = []
            for td in tr.find_all('td'):
                License_info.append(td.get_text().strip(' '))
            data_dict['License'] = License_info
        elif th == 'Categories':
            Categories_info = []
            for td in tr.find_all('td'):
                Categories_info.append(td.get_text().strip(' '))
            data_dict['Categories'] = Categories_info

        elif th == 'Tags':
            Tags_info = []
            for td in tr.find_all('td'):
                for a in td.find_all('a'):
                    print(a)
                    Tags_info.append(a.get_text().strip(' '))
            data_dict['Tags'] = Tags_info


    print(data_dict)

def main():
    html = read()
    data_dict = bs4_paraser(html)
    # print(data_dict)

if __name__ == '__main__':
    main()

