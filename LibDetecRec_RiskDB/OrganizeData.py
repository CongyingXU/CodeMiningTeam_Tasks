#!/usr/bin/env python
# encoding: utf-8
"""

Created on 2019/12/19 17:10
@Author : CongyingXu

"""
import xlrd,json
from CommonFunction import ExcelFiles_Read

def readExcel_byFullpath(Fullpath,col_len):

    wb = xlrd.open_workbook(filename=Fullpath)#打开文件
    print(wb.sheet_names())#获取所有表格名字

    data_dict = {}
    for name in wb.sheet_names():
        data_dict[name] = []
        sheet2 = wb.sheet_by_name(name)  # 通过名字获取表格
        for row in range(sheet2.nrows):
            data_dict[name].append([])
            for col in range(col_len):
                cell_value = sheet2.cell(row,col).value
                data_dict[name][row].append(cell_value)
    return data_dict


    #     sheet1 = wb.sheet_by_index(0)#通过索引获取表格
    #     sheet2 = wb.sheet_by_name('年级')#通过名字获取表格
    #     print(sheet1,sheet2)
    #     print(sheet1.name,sheet1.nrows,sheet1.ncols)
    #
    #     rows = sheet1.row_values(2)#获取行内容
    #     cols = sheet1.col_values(3)#获取列内容
    #     print(rows)
    #     print(cols)
    #
    #     print(sheet1.cell(1,0).value)#获取表格里的内容，三种方式
    #     print(sheet1.cell_value(1,0))
    #     print(sheet1.row(1)[0].value)

class organizeData:
    def read_data(self):
        return readExcel_byFullpath('Top100--libraries.xlsx',4)


    def organize_data(self,data_dict):
        result_dict = []
        for key in data_dict.keys():
            for row in range( len(data_dict[key]) ):
                tracker = data_dict[key][row][3]
                if tracker == 'JIRA':
                    gid = data_dict[key][row][0].split(' ')[0].strip('﻿').strip(' ')
                    aid = data_dict[key][row][0].split(' ')[1].strip('﻿').strip(' ')
                    url = data_dict[key][row][2]
                    result_data_dict = {}
                    result_data_dict['groupId'] = gid
                    result_data_dict['artifactId'] = aid
                    result_data_dict['trackerUrl'] = url
                    result_data_dict['repoUrl'] = ''
                    result_dict.append(result_data_dict)
        return result_dict



    def write_date(self,result_dict):
        with open('GA-TrackerRepo-Map.json','w') as f:
            f.write( json.dumps(result_dict,indent=4) )

    def main(self):
        data_dict = self.read_data()
        result_dict = self.organize_data(data_dict)
        self.write_date(result_dict)
        print('test')

if __name__ == '__main__':
    organizeData().main()