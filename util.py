#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 工具
@file_name: util.py
@project: work
@version: 1.0
@date: 2019/1/11 13:45
@author: air
"""

__author__ = 'air'

import re


def table_name_standardize(table_name):
    """
    标准化表名
    FactDiseaseipHis -> FACT_DISEASEIP_HIS
    SpecialDisease_OUT_XTandDP -> SPECIAL_DISEASE_OUT_XTANDDP
    :param table_name: 传入驼峰式命名/下划线命名
    :return: table_name: 返回标准的表命名
    """
    has_underline = (table_name.find('_') > 0)
    table_name_list = []
    if has_underline:
        table_name_list = table_name.split('_')
    else:
        table_name_list.append(table_name)
    table_name = ''
    for item in table_name_list:
        pattern = re.compile('[A-Z]{2,}')
        is_item_modify = pattern.match(item)
        if not is_item_modify:
            pattern = re.compile('([A-Z][a-z]*)')
            table_name += '_'.join(pattern.findall(item)).upper()
            table_name += '_'
        else:
            table_name += item + '_'
    is_underline_end = (table_name.rfind('_') == (table_name.__len__() - 1))
    if is_underline_end:
        table_name = table_name[:-1]
    return table_name


def entity_attributes_standardize(entity_name):
    """
    标准化属性
    :param entity_name: 传入字段字符串
    :return:
    """
    if not entity_name:
        return None
    entity_name = entity_name.strip()
    return entity_name[0].lower() + entity_name.title().replace('_', '')[1:]


def up_case_first_letter(s):
    """
    将第一个字母大写, 其余不变
    :param s:
    :return:
    """
    if not s:
        return None
    return s[0].upper() + s[1:]


def low_case_first_letter(s):
    """
    将第一个字母小写, 其余不变
    :param s:
    :return:
    """
    if not s:
        return None
    return s[0].lower() + s[1:]
