#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 创建jsp文件, 采用easyUI显示表格
@file_name: create_jsp.py
@project: work_templates
@version: 1.0
@date: 2019/3/8 14:51
@author: air
"""

__author__ = 'air'

import time
import util


def create_jsp(entity_name, package_name='medicare', columns_file='output.txt', comments_file='comment.txt'):
    """
    生成jsp文件
    :param entity_name: 实体类名
    :param package_name: 包名
    :param columns_file: 传入字段名文件
    :param comments_file: 传入注释名文件
    :return:
    """
    entity_name = util.low_case_first_letter(entity_name)
    file_name = entity_name + 'List.jsp'
    url = package_name + '/' + entity_name
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write('<%--\n')
        f.write('  User: liji@gz-yibo.com\n')
        f.write('  Date: ' + time.strftime("%Y/%m/%d", time.localtime()))
        f.write('\n  Time: ' + time.strftime("%H:%M", time.localtime()))
        f.write('\n--%>\n')
        f.write('<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>\n')
        f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" '
                '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n')
        f.write('<html xmlns="http://www.w3.org/1999/xhtml">\n')
        f.write('<head>\n')
        f.write('    <title></title>\n')
        f.write('    <%@include file="/WEB-INF/views/include/head.jsp" %>\n')
        f.write('    <style>\n')
        f.write('        #searchForm table{\n')
        f.write('            width: 100%;\n')
        f.write('        }\n')
        f.write('        #searchForm table tr td,\n')
        f.write('        #searchForm table tr th\n')
        f.write('        {\n')
        f.write('            padding: 5px;\n')
        f.write('        }\n')
        f.write('        #searchForm table tr td input{\n')
        f.write('            width: 90%;\n')
        f.write('            margin-right: 15px;\n')
        f.write('        }\n')
        f.write('        #searchForm table tr th{\n')
        f.write('            width: 80px;\n')
        f.write('            padding-left:10px;\n')
        f.write('            text-align: right;\n')
        f.write('        }\n')
        f.write('        th{\n')
        f.write('            font-weight: normal;\n')
        f.write('        }\n')
        f.write('        .breadcrumb{\n')
        f.write('            padding-left:0;\n')
        f.write('            margin-bottom: 0;\n')
        f.write('        }\n')
        f.write('        #searchForm table tr td input.search-btn{\n')
        f.write('            width: 80%;\n')
        f.write('            margin: 0;\n')
        f.write('        }\n')
        f.write('        #searchForm table tr td input.combo-text{\n')
        f.write('            margin-right: 0;\n')
        f.write('        }\n')
        f.write('    </style>\n')
        f.write('    <script type="text/javascript">\n\n')
        f.write('        $(function () {\n')
        f.write('            $(\'#dataTable\').datagrid({\n')
        f.write('                rownumbers: true,\n')
        f.write('                loading: true,\n')
        f.write('                fit: true,\n')
        f.write('                toolbar: "#dataTableBar",\n')
        f.write('                url: \'${ctx}/' + url + '/list.do\',\n')
        f.write('                pagination: true,\n')
        f.write('                pageSize: 20,\n')
        f.write('                columns: [[\n')
        with open(columns_file, 'r', encoding='utf-8') as f2:
            fields = f2.readlines()
        with open(comments_file, 'r', encoding='utf-8') as f3:
            titles = f3.readlines()
        for i in range(len(fields)):
            f.write('                    {field: \'' + util.entity_attributes_standardize(fields[i])
                    + '\', title: \'' + titles[i].strip() + '\', width: 120},\n')
        f.write('                ]]\n            });\n\n')
        f.write('            new CrudForm({datagrid: \'dataTable\'});\n\n')
        f.write('            $("#search").click(function() {\n')
        f.write('                $(\'#dataTable\').datagrid("load", yibo.util.formJson($("#searchForm")));\n')
        f.write('            });\n        });\n')
        f.write('    </script>\n</head>\n')
        f.write('<body class="easyui-layout">\n')
        f.write('<div data-options="region:\'center\'" style="padding:0px;border:0px;" data-options="fit:true">\n')
        f.write('    <table id="dataTable"></table>\n')
        f.write('    <div id="dataTableBar">\n')
        f.write('        <a class="easyui-linkbutton" id="tool-search-btn" '
                'data-options="plain: true, iconCls: \'layout-button-up\'">查询</a>\n')
        f.write('        <!-- 查询条件 -->\n')
        f.write('        <form id="searchForm" class="breadcrumb form-search" style="display:none" method="post">\n')
        f.write('            <table>\n')
        f.write('                <tr>\n')
        f.write('                    <td style="text-align: center"><input id="search" '
                'class="btn btn-primary search-btn" type="button" value="查询" style="line-height:15px"/></td>\n')
        f.write('                </tr>\n')
        f.write('            </table>\n')
        f.write('        </form>\n')
        f.write('    </div>\n</div>\n</body>\n</html>\n\n')


def create_search(search_file="search.txt"):
    """
    添加搜索条件
    :param search_file: 搜索条件文本文件
    :return:
    """
    with open('search.jsp', 'w', encoding='utf-8') as f:
        with open(search_file, 'r', encoding='utf-8') as f2:
            search = f2.readlines()
        for i in range(len(search)):
            item = search[i].split(' ')
            item[-1] = util.entity_attributes_standardize(item[-1].strip())
            if i % 3 == 0:
                f.write('                <tr>\n')
            f.write('                    <th>' + item[0] + ':</th>\n')
            f.write('                    <td><input type="text" name="' + item[-1] + '" id="' + item[-1] + '"/></td>\n')
            if i % 3 == 2:
                f.write('                </tr>\n')
        if len(search) % 3 != 0:
            f.write('                </tr>\n')
