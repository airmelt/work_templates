#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 检查是否为xls文件
@file_name: xls_test.py
@project: work
@version: 1.0
@date: 2019/11/21 14:00
@author: air
"""

import xlrd


data = xlrd.open_workbook('201810特殊病种.xls')
# data = xlrd.open_workbook('特殊病种test.xls')
table = data.sheets()[0]
print(table.cell(0, 0).value)
