#!/usr/bin/env python
# encoding: utf-8
"""

Created on 2019/8/21 14:42
@Author : CongyingXu

该py,单独用于一切 读取excels的文件块
"""

import xlrd

def readExcel_byFullpath(Fullpath):

    wb = xlrd.open_workbook(filename=Fullpath)#打开文件
    print(wb.sheet_names())#获取所有表格名字

    # sheet1 = wb.sheet_by_index(0)#通过索引获取表格
    # sheet2 = wb.sheet_by_name('年级')#通过名字获取表格
    # print(sheet1,sheet2)
    # print(sheet1.name,sheet1.nrows,sheet1.ncols)
    #
    # rows = sheet1.row_values(2)#获取行内容
    # cols = sheet1.col_values(3)#获取列内容
    # print(rows)
    # print(cols)
    #
    # print(sheet1.cell(1,0).value)#获取表格里的内容，三种方式
    # print(sheet1.cell_value(1,0))
    # print(sheet1.row(1)[0].value)

if __name__ == '__main__':
    readExcel_byFullpath('/c/Users/Congy/PycharmProjects/CodeMiningTeam_Tasks/LibDetecRec_RiskDB/Top100--libraries.xlsx')