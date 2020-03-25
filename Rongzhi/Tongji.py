# -*- coding: utf-8 -*-

"""
Created on 2020-03-06 09:23  

@author: congyingxu
"""

from CommonFunction import ExcelFiles_Read, ExcelFiles_Write

excel1_path = "/Users/congyingxu/Downloads/CodeMiningTeam_Tasks/Rongzhi/1.xls"
excel2_path = "/Users/congyingxu/Downloads/CodeMiningTeam_Tasks/Rongzhi/2.xlsx"
result_path = "/Users/congyingxu/Downloads/CodeMiningTeam_Tasks/Rongzhi/result.xls"

excel1 = {}
excel2 = {}

result = {"身份证号查找":[ ],"姓名查找":[ ],"姓名+证号一致":[]}
title_list1 = ["身份证号","姓名1 基础信息","地址1","姓名不一致","姓名2 补助总表","地址2"]
result["身份证号查找"].append(title_list1  )

title_list2 = ["姓名","身份证号1 基础信息","地址1","证号不一致","身份证号2 补助总表","地址2"]
result["姓名查找"].append(title_list2  )

title_list3 = ["姓名","身份证号","地址1 基础信息","地址2 补助总表"]
result["姓名+证号一致"].append(title_list3  )



def read():
    global excel1, excel2
    excel1 = ExcelFiles_Read.readExcel_byFullpath(excel1_path).sheet_by_name('1')
    excel2 = ExcelFiles_Read.readExcel_byFullpath(excel2_path).sheet_by_name('2')

def collectData():
    global result

    sheet1_name_list = excel1.col_values(2)[1:]
    sheet1_id_list = excel1.col_values(6)[1:]
    sheet1_address_list = excel1.col_values(5)[1:]

    print(len(sheet1_name_list),len(sheet1_id_list),len(sheet1_address_list))

    sheet2_name_list = excel2.col_values(1)[2:]
    sheet2_id_list = excel2.col_values(2)[2:]
    sheet2_address_list = excel2.col_values(4)[2:]

    # print(sheet2_address_list)
    print(len(sheet2_name_list), len(sheet2_id_list), len(sheet2_address_list))

    for id in sheet1_id_list:
        if id in sheet2_id_list:
            # print(id)
            index1 = sheet1_id_list.index(id)
            name1 = sheet1_name_list[index1]
            address1 = sheet1_address_list[index1]

            index2 = sheet2_id_list.index(id)
            name2 = sheet2_name_list[index2]
            address2 = sheet2_address_list[index2]


            if name1 == name2:
                result["身份证号查找"].append( [id, name1,address1,"",name2,address2] )
                result["姓名+证号一致"].append([name1, id, address1, address2])
            else:
                # print(id)
                result["身份证号查找"].append( [id, name1,address1,"不一致",name2,address2] )

    for name in sheet1_name_list:
        if name in sheet2_name_list:
            # print(id)
            index1 = sheet1_name_list.index(name)
            id1 = sheet1_id_list[index1]
            address1 = sheet1_address_list[index1]

            index2 = sheet2_name_list.index(name)
            id2 = sheet2_id_list[index2]
            address2 = sheet2_address_list[index2]


            if id1 == id2:
                result["姓名查找"].append( [name, id1,address1,"",id2,address2] )
            else:
                print(name)
                result["姓名查找"].append( [name, id1,address1,"不一致",id2,address2] )





    # for index in range( excel1.nrows )[1:]:
    #     name1 = excel1.cell(index, 2).value
    #     print(excel1.cell(index, 2).value)
    #     break

def write():
    ExcelFiles_Write.wirte_ByDictList(result_path,result,[])


if __name__ == '__main__':
    read()
    collectData()
    write()