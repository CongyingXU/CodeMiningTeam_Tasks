# -*- coding: utf-8 -*-

"""
Created on 2019-12-02 18:41  

@author: congyingxu

https://mvnrepository.com/artifact/junit/junit/4.13-rc-2
"""


from bs4 import BeautifulSoup

def read():
    with open('ArtifactsHomepage_test.html','r') as f:
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
        td = tr.find_all('td')[0].string
        # print(th,td)
        # print()

        # if th == 'License':
        #     data_dict['License'] = td
        # elif th == 'Categories':
        #     data_dict['Categories'] = td
        # elif th == 'Date':
        #     data_dict['Date'] = td

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

        elif th == 'Date':
            Date_info = []
            for td in tr.find_all('td'):
                    Date_info.append(td.get_text().strip(' '))
            data_dict['Date'] = Date_info


    developers_info = []
    lisence_info = []
    for title in div.find_all('div', attrs={'class': 'version-section'}):
        h2 = title.find('h2')
        # print(h2)

        if h2 == None:
            continue

        if h2.get_text() == 'Developers':

            for tr in title.find_all('tbody')[0].find_all('tr'):
                td_list = tr.find_all('td')
                Name = td_list[0].get_text()
                Email = td_list[1].get_text()
                Dev_Id = td_list[2].get_text()
                Roles = td_list[3].get_text()
                Organization = td_list[4].get_text()

                developers_info.append( (Name,Email,Dev_Id,Roles,Organization) )
                # print( (Name,Email,Dev_Id,Roles,Organization) )
        elif h2.get_text() == 'Licenses':
            for tr in title.find_all('tbody')[0].find_all('tr'):
                td_list = tr.find_all('td')
                License = td_list[0].get_text()
                URL = td_list[1].get_text().strip('\n')

                lisence_info.append( (License,URL) )
                # print( (License,URL) )
        data_dict['lisence_info'] = lisence_info
        data_dict['developers_info'] = developers_info


    print(data_dict)




def main():
    html = read()
    data_dict = bs4_paraser(html)
    # print(data_dict)

if __name__ == '__main__':
    main()

