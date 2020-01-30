#!/usr/bin/env python
# encoding: utf-8
"""

Created on 2020/1/12 10:15
@Author : CongyingXu

"""

from terminaltables import AsciiTable
table_data = [ ['Heading1', 'Heading2'], ['row1 column1', 'row1 column2'], ['row2 column1', 'row2 column2'], ['row3 column1', 'row3 column2'] ]
table = AsciiTable(table_data)
print(table.table)

# +--------------+--------------+ | Heading1 | Heading2 | +--------------+--------------+ | row1 column1 | row1 column2 | | row2 column1 | row2 column2 | | row3 column1 | row3 column2 | +--------------+--------------+


from terminaltables import PorcelainTable
table_data = [ ['Heading1', 'Heading2'], ['row1 column1', 'row1 column2'], ['row2 column1', 'row2 column2'], ['row3 column1', 'row3 column2'] ]
table = PorcelainTable(table_data)
print(table.table)