# -*- coding: utf-8 -*-

"""
Created on 2020-04-04 12:05  

@author: congyingxu

用于解析并收集所有SID的模块信息

Meta-Module：


Publish Date : 2019-01-18
Last Update Date : 2019-08-21

CVSS Score
Confidentiality Impact
Integrity Impact
Availability Impact
Access Complexity
Authentication
Gained Access
Vulnerability Type(s)
CWE ID


Vendor Statements(0)
Additional Vendor Data(0)
OVAL Definitions(0)


Affected Products
Number Of Affected Versions
References
Vulnerability Conditions
Metasploit Modules

"""

from CommonFunction import JSONFIle_processing, File_processing
from bs4 import BeautifulSoup


CVEDetails_pages_dir = "/Users/congyingxu/Downloads/CVE/CrawledCVEdetailsHtmls/Pages/"
CVEDetailsItems_dir = "/Users/congyingxu/Downloads/CVE/CrawledCVEdetailsHtmls/CVEDetailsItems/"

CVEDetails_CVEID_list = []
CVEDetails_CVEID_list_path = "/Users/congyingxu/Downloads/CVE/MetaData/CVEDetails_CVEID_list.json"


CVE_CVEID_list_path = "/Users/congyingxu/Downloads/CVE/MetaData/CVE_CVEID_list.json"
CVE_CVEID_list = JSONFIle_processing.read(CVE_CVEID_list_path)


log_item_info = False


def extractItem(CVEID):
    global CVEDetails_CVEID_list,CVEDetailsItems_dir
    path = CVEDetails_pages_dir + CVEID + 'atCVEDetails.html'
    html = File_processing.read_TXTfile(path)

    # CVEID not in CVEdetails Unknown CVE ID
    if "Unknown CVE ID" in html:
        # print("Unknown CVE ID",CVEID)
        return



    soup = BeautifulSoup(html, 'lxml')
    item_info = {}

    # Publish Date : 2019-01-18
    # Last Update Date : 2019-08-21
    div = soup.find('div', attrs={'class': 'cvedetailssummary'})
    desc = div.contents[0].replace('\n','').strip('\n').strip('\t')
    span_date = div.find('span', attrs={'class': 'datenote'}).text.replace('\n','').strip('\n').strip('\t')
    item_info['desc'] = desc
    item_info['date'] = span_date.replace('\t','__fdse__')
    if log_item_info:
        print(desc, span_date)

    # CVSS Score
    # Confidentiality Impact
    # Integrity Impact
    # Availability Impact
    # Access Complexity
    # Authentication
    # Gained Access
    # Vulnerability Type(s)
    # CWE ID
    table = soup.find(id = "cvssscorestable")
    if table != None:
        trs = table.find_all('tr')
        for tr in trs:
            th = tr.find('th')
            field = th.text
            td = tr.find('td')
            value = td.text.split('\n')

            item_info[field] = value
            if log_item_info:
                print(field, value)


    # print(table)


    # Vendor Statements(0)
    table = soup.find(id="vendorstatementsdiv")
    if table != None:
        div = soup.find('div', attrs={'class': 'vendorstatement'})
        VendorStatements = div.contents[0]
        VendorStatements_span =  div.find('span').text.replace('\n','').replace('\t','')
        if div.find('a') != None:
            VendorStatements_span_url = div.find('a')["href"].strip('/')
        else:
            VendorStatements_span_url = ''
        if len(div.find_all('a') ) >1:
            print("Eeeeeeeeeeeeeeeeeeeeeeeeerror: len(div.find_all('a') ) >1")

        item_info["Vendor Statements"] = VendorStatements.replace('\n','').strip('\n').strip('\t')
        item_info["Vendor Statements source"] = [VendorStatements_span + "__fdse__" + VendorStatements_span_url]
    else:
        item_info["Vendor Statements"] = None
        item_info["Vendor Statements source"] =None
    if log_item_info:
        print("---------------Vendor Statements", item_info["Vendor Statements"])
        print("---------------Vendor Statements source", item_info["Vendor Statements source"])


    # Additional Vendor Data(0)
    addtional_vendor_data = []
    div = soup.find(id="addvendsuppdata")
    if div != None:
        table = div.find('table', attrs={'class': 'listtable'})
        trs = table.find_all('tr')
        for tr in trs:

            tds = tr.find_all('td')
            ths = tr.find_all('th')
            record = []
            for td in tds:
                if td.find('a') != None:  # 有链接
                    oval_url = td.find('a')['href']
                    record.append(td.text.strip('\n').strip('\t') + '__fdse__' + oval_url)
                else:
                    record.append(td.text.strip('\n').strip('\t'))
            for th in ths:
                record.append(th.text.strip('\n').strip('\t').strip('\n'))

            addtional_vendor_data.append(record)
        item_info["Additional Vendor Data"] = addtional_vendor_data
    else:
        item_info["Additional Vendor Data"] = None
    if log_item_info:
        print("---------------Additional Vendor Data" ,item_info["Additional Vendor Data"] )

    # OVAL Definitions(0)
    oval = []
    div = soup.find(id="ovaldefsmaindiv")
    if div != None:
        tbody = div.find('table',attrs={'class':'listtable'})
        trs = tbody.find_all('tr')
        for tr in trs:

            tds = tr.find_all('td')
            ths = tr.find_all('th')
            record = []
            for td in tds:
                if td.find('a') != None:  # 有链接
                    oval_url = td.find('a')['href']
                    record.append(td.text.strip('\n').strip('\t') + '__fdse__' + oval_url)
                else:
                    record.append(td.text.strip('\n').strip('\t'))
            for th in ths:
                record.append(th.text.strip('\n').strip('\t').strip('\n'))

            oval.append( record )
        item_info["OVAL Definitions"] = oval
    else:
        item_info["OVAL Definitions"] = None
    if log_item_info:
        print("---------------OVAL Definitions", item_info["OVAL Definitions"] )


    # Affected Products
    affected_products = []
    table = soup.find(id="vulnprodstable")
    if table != None:
        trs = table.find_all('tr')
        for tr in trs:

            tds = tr.find_all('td')
            ths = tr.find_all('th')
            record = []
            for td in tds:
                record.append(td.text.strip('\n').strip('\t').strip('\n'))
            for th in ths:
                record.append(th.text.strip('\n').strip('\t').strip('\n'))
            affected_products.append(record)
        item_info["Affected Products"] = affected_products
    else:
        item_info["Affected Products"] = None
    if log_item_info:
        print("---------------Affected Products", item_info["Affected Products"])


    # Number Of Affected Versions
    affected_Versions = []
    table = soup.find(id="vulnversconuttable")
    if table != None:
        trs = table.find_all('tr')
        for tr in trs:

            tds = tr.find_all('td')
            ths = tr.find_all('th')
            record = []
            for td in tds:
                record.append(td.text.strip('\n').strip('\t').strip('\n'))
            for th in ths:
                record.append(th.text.strip('\n').strip('\t').strip('\n'))

            affected_Versions.append(record)
        item_info["Number Of Affected Versions"] = affected_Versions
    else:
        item_info["Number Of Affected Versions"] = None
    if log_item_info:
        print("---------------Number Of Affected Versions",item_info["Number Of Affected Versions"])

    # References
    item_info["References"] = []
    table = soup.find(id="vulnrefstable")
    if table != None:
        trs = table.find_all('tr')
        for tr in trs:
            full_url = tr.text.strip('\n').strip('\t')
            item_info["References"].append(full_url)
    else:
        item_info["References"] = None
    if log_item_info:
        print("---------------References",item_info["References"])

    # Vulnerability Conditions
    item_info["Vulnerability Conditions"] = []
    table = soup.find(id="vulncondstable")
    if table != None:
        trs = table.find_all('tr')
        condi_record = []
        for tr in trs:
            tds = tr.find_all('td')
            for td in tds:

                if td.find('li') == None:
                    if td.find('a') != None:  # 有链接
                        oval_url = td.find('a')['href']
                        condi_record.append(td.text.replace('\n',' ').replace('\t','').strip('\n').strip('\t') + '__fdse__' + oval_url)
                    else:
                        condi_record.append(td.text.replace('\n',' ').replace('\t','').strip('\n').strip('\t'))
                else:
                    lis = td.find_all('li')
                    lis_record = []
                    for li in lis:
                        if li.find('a') != None:  # 有链接
                            oval_url = li.find('a')['href']
                            lis_record.append(li.text.replace('\n', ' ').replace('\t', '').strip('\n').strip(
                                '\t') + '__fdse__' + oval_url)
                        else:
                            lis_record.append(li.text.replace('\n', ' ').replace('\t', '').strip('\n').strip('\t'))
                    condi_record.append(lis_record)
        item_info["Vulnerability Conditions"] = condi_record
    else:
        item_info["Vulnerability Conditions"] = None
    if log_item_info:
        print("---------------Vulnerability Conditions",item_info["Vulnerability Conditions"])

    # Metasploit Modules
    MetasploitModules = []
    item_info["Metasploit Modules"] = []
    div = soup.find(id="metasploitmodstable")
    table = div.find('table', attrs={'class': 'metasploit'})
    if table != None:
        trs = table.find_all('tr')
        for tr in trs:
            if tr.find('a') != None:  # 有链接
                oval_url = tr.find('a')['href']
                MetasploitModules.append(tr.text.replace('\n', '').replace('\t', '').strip('\n').strip(
                    '\t') + '__fdse__' + oval_url)
            else:
                MetasploitModules.append(tr.text.replace('\n', '').replace('\t', '').strip('\n').strip('\t'))

            item_info["Metasploit Modules"] = MetasploitModules
    else:
        item_info["Metasploit Modules"] = None
    if log_item_info:
        print("---------------Metasploit Modules", item_info["Metasploit Modules"])


    # print('--------------------------------------------------------------')
    # print()
    # print(item_info)

    CVEDetails_CVEID_list.append(CVEID)
    item_path = CVEDetailsItems_dir + CVEID +'.json'
    JSONFIle_processing.write(json_content=item_info,path=item_path)





def main():
    global CVEDetails_CVEID_list, CVEDetailsItems_dir
    for CVEID in CVE_CVEID_list:
        print(CVEID)
        extractItem(CVEID)

        # extractItem("CVE-2004-1864")
        # break

    JSONFIle_processing.write(CVEDetails_CVEID_list,CVEDetails_CVEID_list_path)

if __name__ == '__main__':
    main()
