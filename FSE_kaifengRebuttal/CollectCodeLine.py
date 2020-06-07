# -*- coding: utf-8 -*-

"""
Created on 2020-04-30 17:06  

@author: congyingxu

用于统计不同项目的代码行数
"""

from CommonFunction import File_processing, ExcelFiles_Read

cloc_dir = '/Users/congyingxu/Downloads/cloc/'
category_path = '/Users/congyingxu/Downloads/category-total.xlsx'
poj_order = []

def readExcel():
    global poj_order
    wb = ExcelFiles_Read.readExcel_byFullpath(category_path)
    sheet1 = wb.sheet_by_index(0)
    poj_order = sheet1.col_values(1)
    poj_order = poj_order[1:]
    # print(poj_order)
    # for index in range( sheet1.nrows ):
    #     print( sheet1.sheet1.col_values(3) )

def getCodeLineNum(poj_name):
    poj_path = cloc_dir + poj_name
    # print(poj_path)
    content = File_processing.read_TXTfile(poj_path)
    Num = content.split('\n')[-3].split('          ')[-1]
    Num = content.split('\n')[-3].split(' ')[-1]
    # print( content.split('\n')[-3] )
    # print(content.split('\n')[-3].split('          ')[-1])
    # print(poj_name, Num)
    return Num



def main():
    readExcel()
    poj_list = File_processing.walk_L1_FileNames(cloc_dir)
    poj_CodelineNum_dict = {}
    for poj_name in poj_list:
        poj_CodelineNum_dict[poj_name.split('.txt')[0]] = getCodeLineNum(poj_name)
        # break

    # print(poj_CodelineNum_dict)
    print(poj_CodelineNum_dict)
    NA = 0
    for ele in poj_order:
        if ele in poj_CodelineNum_dict.keys():
            # print(ele,poj_CodelineNum_dict[ele])
            print(poj_CodelineNum_dict[ele])
        else:
            # print(ele, 'NA')
            print('NA')
            NA +=1
    print('NA',NA)


if __name__ == '__main__':
    main()
