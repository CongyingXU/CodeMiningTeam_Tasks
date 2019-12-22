#!/usr/bin/env python
# encoding: utf-8
"""

Created on 2019/8/21 14:42
@Author : CongyingXu

该py,单独用于一切 写excels的文件块
"""

import xlwt


Data_dict_list = {}
# 该函数用于写excel文件
# 参数：
# file_dir：文件全名,Data_dict_list：数据,title_list：第一行的标题行
# 数据格式为：{'sheet':[ [row0], [row1] ... ]}
def wirte_ByDictList(file_dir,Data_dict_list,title_list):
    workbook = xlwt.Workbook(encoding='utf8')
    for sheet_name in Data_dict_list.keys():
        worksheet = workbook.add_sheet(sheet_name)

        row_index = 0
        # 标题行处理
        if len(title_list) > 0:
            for ele_column_index in range(len(title_list)):
                worksheet.write(0, ele_column_index, title_list[ele_column_index])
            row_index+=1

        for row_data_list in Data_dict_list[sheet_name]:
            # row_data_list：每一行的数据，形式为list
            for ele_column_index in range(len(row_data_list)):
                # ele_column_index:列的数据
                # print(1111)
                # print(row_index, ele_column_index,row_data_list[ele_column_index].value)
                worksheet.write(row_index, ele_column_index, row_data_list[ele_column_index])
            row_index+=1

    workbook.save(file_dir)
