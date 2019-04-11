#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 新建sql语句文件/create sql file
@file_name: create_sql.py
@project: work
@version: 1.0
@date: 2019/1/11 13:45
@author: air
"""

__author__ = 'air'

import pandas as pd
import re


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
    # 读取字段及注释
    with open(columns_file, 'r', encoding='utf-8') as f1, open(comment_file, 'r', encoding='utf-8') as f2:
        columns = f1.readlines()
        comments = f2.readlines()
    with open(table_name + '.sql', 'w', encoding='utf-8') as f3:
        f3.write("CREATE TABLE [dbo].[" + table_name + "] (\n")
        f3.write("  [PK_ID] int  IDENTITY(1,1) NOT NULL,\n")
        for i in range(columns.__len__()):
            f3.write("  [" + columns[i].strip() + "] varchar(255) COLLATE Chinese_PRC_CI_AS NULL,\n")
        f3.write("  [FCreateUser] varchar(255) COLLATE Chinese_PRC_CI_AS NULL,\n")
        f3.write("  [FYearMonth] varchar(255) COLLATE Chinese_PRC_CI_AS NULL,\n")
        f3.write("  PRIMARY KEY CLUSTERED ([PK_ID])\n")
        f3.write("WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, "
                 "IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)\n")
        f3.write(")\nGO\n\n")
        f3.write("EXEC sp_addextendedproperty\n")
        f3.write("'MS_Description', N'主键',\n")
        f3.write("'SCHEMA', N'dbo',\n")
        f3.write("'TABLE', N'" + table_name + "',\n")
        f3.write("'COLUMN', N'PK_ID'\n")
        f3.write("GO\n\n")
        for i in range(columns.__len__()):
            f3.write("EXEC sp_addextendedproperty\n")
            f3.write("'MS_Description', N'" + comments[i].strip() + "',\n")
            f3.write("'SCHEMA', N'dbo',\n")
            f3.write("'TABLE', N'" + table_name + "',\n")
            f3.write("'COLUMN', N'" + columns[i].strip() + "'\n")
            f3.write("GO\n\n")
        f3.write("EXEC sp_addextendedproperty\n")
        f3.write("'MS_Description', N'数据创建用户',\n")
        f3.write("'SCHEMA', N'dbo',\n")
        f3.write("'TABLE', N'" + table_name + "',\n")
        f3.write("'COLUMN', N'FCreateUser'\n")
        f3.write("GO\n\n")
        f3.write("EXEC sp_addextendedproperty\n")
        f3.write("'MS_Description', N'年月',\n")
        f3.write("'SCHEMA', N'dbo',\n")
        f3.write("'TABLE', N'" + table_name + "',\n")
        f3.write("'COLUMN', N'FYearMonth'\n")
        f3.write("GO\n\n")
        f3.write("EXEC sp_addextendedproperty\n")
        f3.write("'MS_Description', N'" + table_comment + "',\n")
        f3.write("'SCHEMA', N'dbo',\n")
        f3.write("'TABLE', N'" + table_name + "'\n")


def create_add_sql(table_name, columns_file='output.txt', comment_file='comment.txt'):
    """
    输出追加SQL字段sql语句文件
    :param table_name: 表名
    :param columns_file: 传入表字段名文件, 默认为 output.txt
    :param comment_file: 传入表字段注释文件, 默认为 comment.txt
    :return:
    """
    # 读取字段及注释
    with open(columns_file, 'r', encoding='utf-8') as f1, open(comment_file, 'r', encoding='utf-8') as f2:
        columns = f1.readlines()
        comments = f2.readlines()
    with open(table_name + '.sql', 'w', encoding='utf-8') as f3:
        for i in range(columns.__len__()):
            f3.write("ALTER TABLE [dbo].[" + table_name + "] ADD[" + columns[i].strip() + "] varchar(255) NULL\n")
            f3.write("GO\n\n")
        for i in range(columns.__len__()):
            f3.write("EXEC sp_addextendedproperty\n")
            f3.write("'MS_Description', N'" + comments[i].strip() + "',\n")
            f3.write("'SCHEMA', N'dbo',\n")
            f3.write("'TABLE', N'" + table_name + "',\n")
            f3.write("'COLUMN', N'" + columns[i].strip() + "'\n")
            f3.write("GO\n\n")


def mdx2update_sql(input_file, table_name):
    """
    mdx语句转换成sql的update语句
    :param input_file:
    :param table_name:
    :return:
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        with open(input_file.replace('.txt', '_output.txt'), 'w', encoding='utf-8') as f2:
            line = f.readline()
            while line:
                code_pattern = re.compile('\[Measures\].\[(.*)\]\s+AS')
                indicator_code = code_pattern.findall(line)[0]
                mdx_pattern = re.compile('AS\s+(.*)\s+,')
                mdx_magnitude = mdx_pattern.findall(line)[0].strip()
                format_pattern = re.compile('"(.*)"')
                format_string = format_pattern.findall(line)[0]
                sql = "UPDATE " + table_name + " SET MDX_MAGNITUDE = '" + \
                      mdx_magnitude + "', FORMAT_STRING = '" + format_string + \
                      "' , YEAR_ON_YEAR_FLAG = '1', RING_RATIO_FLAG = '1' WHERE INDICATOR_CODE = '" + \
                      indicator_code + "';\n"
                f2.write(sql)
                line = f.readline()


def mdx2insert_sql(input_file, comment_file, table_name, table_id):
    """
    将mdx语句转换成sql的insert语句
    :param input_file: 传入文件
    :param comment_file: 字段注释文件
    :param table_name: 表名
    :param table_id: 表编号
    :return:
    """
    with open(input_file, 'r', encoding='utf-8') as f, open(comment_file, 'r', encoding='utf-8') as f2:
        with open(input_file.replace('.txt', '_output.txt'), 'w', encoding='utf-8') as f3:
            line = f.readline()
            indicator_name = f2.readline().strip()
            i = 30
            while line:
                code_pattern = re.compile('\[Measures\].\[(.*)\]\s+AS')
                indicator_code = code_pattern.findall(line)[0]
                mdx_pattern = re.compile('AS\s+(.*)\s+,')
                mdx_magnitude = mdx_pattern.findall(line)[0].strip()
                format_pattern = re.compile('"(.*)"')
                format_string = format_pattern.findall(line)[0]
                # insert into table_name (a, b) values ('', '')
                sql = "INSERT INTO " + table_name + \
                      " (INDICATOR_NAME, INDICATOR_CODE, MDX_MAGNITUDE, FORMAT_STRING, " \
                      "YEAR_ON_YEAR_FLAG, RING_RATIO_FLAG, SERIAL_NUMBER, STATUS, LEVEL, TABLE_ID) " \
                      "VALUES ('" + indicator_name + "', '" + indicator_code + "', '" + mdx_magnitude + \
                      "', '" + format_string + "', '1', '1', '" + str(i) + "', '1', '1', '" + table_id + \
                      "');\n"
                i = i + 1
                f3.write(sql)
                line = f.readline()
                indicator_name = f2.readline().strip()


if __name__ == '__main__':
    # excel2txt(r'201801新版职工.XLS', 3, 1)
    # create_sql('STAFF_MEDICARE_INSURANCE', '职工医疗保险定点结算表')
    # mdx2update_sql('mdx_HIS.txt', 'INDICATOR_MANAGEMENT')
    mdx2insert_sql('mdx_SCORE.txt', 'comment_score.txt', 'INDICATOR_MANAGEMENT', '2')
