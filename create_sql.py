#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 新建sql语句文件
@file_name: create_sql.py
@project: work
@version: 1.0
@date: 2019/1/11 13:45
@author: air
"""

__author__ = 'air'

import pandas as pd
import util


def excel2txt(input_file, row=0, begin_column=0, output_file='comment.txt'):
    """
    提取注释, 即表头
    :param input_file: 传入excel文件
    :param row: 表头所在行数, 默认为 0
    :param begin_column: 开始列数, 默认为 0
    :param output_file: 输出文件名, 默认为 comment.txt
    :return:
    """
    df1 = pd.read_excel(input_file, header=None)
    text_list = list(df1.iloc[row])[begin_column:]
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in text_list:
            # 判断是否为NaN
            if item != item:
                continue
            item = ''.join(item.split())
            f.write(item + '\n')


def create_sql(table_name, table_comment, columns_file='output.txt', comment_file='comment.txt'):
    """
    输出sql语句文件
    :param table_name: 表名
    :param table_comment: 表注释
    :param columns_file: 传入表字段名文件, 默认为 output.txt
    :param comment_file: 传入表字段注释文件, 默认为 comment.txt
    :return:
    """
    # 标准化表名
    table_name = util.table_name_standardize(table_name)
    # 读取字段及注释
    with open(columns_file, 'r', encoding='utf-8') as f1, open(comment_file, 'r', encoding='utf-8') as f2:
        columns = f1.readlines()
        comments = f2.readlines()
    with open(table_name + '.sql', 'w', encoding='utf-8') as f3:
        f3.write("CREATE TABLE [dbo].[" + table_name + "] (\n")
        f3.write("  [PK_ID] int  IDENTITY(1,1) NOT NULL,\n")
        for i in range(columns.__len__()):
            f3.write("  [" + columns[i].strip() + "] varchar(255) COLLATE Chinese_PRC_CI_AS NULL,\n")
        f3.write("  PRIMARY KEY CLUSTERED ([PK_ID])\n")
        f3.write("WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, "
                 "IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)\n")
        f3.write(")\nGO\n\n")
        for i in range(columns.__len__()):
            f3.write("EXEC sp_addextendedproperty\n")
            f3.write("'MS_Description', N'" + comments[i].strip() + "',\n")
            f3.write("'SCHEMA', N'dbo',\n")
            f3.write("'TABLE', N'" + table_name + "',\n")
            f3.write("'COLUMN', N'" + columns[i].strip() + "'\n")
            f3.write("GO\n\n")
        f3.write("EXEC sp_addextendedproperty\n")
        f3.write("'MS_Description', N'" + table_comment + "',\n")
        f3.write("'SCHEMA', N'dbo',\n")
        f3.write("'TABLE', N'" + table_name + "'\n")


if __name__ == '__main__':
    # excel2txt(r'201801新版职工.XLS', 3, 1)
    create_sql('STAFF_MEDICARE_INSURANCE', '职工医疗保险定点结算表')
