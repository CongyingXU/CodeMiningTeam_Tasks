# -*- coding: utf-8 -*-

"""
Created on 2020-02-12 10:48

@author: congyingxu
"""


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

# print( is_number("00000123456789") )


def compared_version(ver1, ver2):
    """
    1、纯数字时，优先用数字比
    2、含有其他字符时，用字符串比
    """

    # 判断是否有其他字符
    tem1 = ver1
    tem2 = ver2

    if is_number( tem1.replace('.','') ) and is_number( tem2.replace('.','') ):
        """
        传入不带英文的版本号,特殊情况："10.12.2.6.5">"10.12.2.6"
        :param ver1: 版本号1
        :param ver2: 版本号2
        :return: ver1< = >ver2返回-1/0/1
        """
        list1 = str(ver1).split(".")
        list2 = str(ver2).split(".")
        # print(list1)
        # print(list2)
        # 循环次数为短的列表的len
        for i in range(len(list1)) if len(list1) < len(list2) else range(len(list2)):
            if int(list1[i]) == int(list2[i]):
                pass
            elif int(list1[i]) < int(list2[i]):
                return -1
            else:
                return 1
        # 循环结束，哪个列表长哪个版本号高
        if len(list1) == len(list2):
            return 0
        elif len(list1) < len(list2):
            return -1
        else:
            return 1

    else:
        if ver1 > ver2:
            return 1
        elif ver1 < ver2:
            return -1
        else:
            return 0