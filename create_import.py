#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 新建导入文件/create file for importing excel
@file_name: create_import.py
@project: work_templates
@version: 1.0
@date: 2019/1/11 23:05
@author: air
"""
import util

__author__ = 'air'


def reader_import(table_name, columns_for_read, start_row_num):
    """
    生成readerHelper文件
    :param table_name: 表名称
    :param columns_for_read: 要读取的excel列数
    :param start_row_num: 要读取的excel开始的行数
    :return:
    """
    entity_name = table_name
    entity_name = util.entity_attributes_standardize(entity_name)
    entity_name = util.up_case_first_letter(entity_name)
    columns_for_read = str(columns_for_read)
    start_row_num = str(start_row_num)
    with open(entity_name + 'ExcelHelper.java', 'w', encoding='utf-8') as f:
        f.write('package com.yibo.modules.medicare.reader;\n\n')
        f.write('import com.yibo.core.common.utils.excel.XLSConvertCSVUtil;\n')
        f.write('import com.yibo.core.common.utils.excel.XLSXCovertCSVUtil;\n')
        f.write('import com.yibo.modules.medicare.dao.' + entity_name + 'Dao;\n')
        f.write('import com.yibo.modules.medicare.entity.FileImport;\n')
        f.write('import com.yibo.modules.medicare.others.WorkConfig;\n')
        f.write('import org.apache.ibatis.session.SqlSession;\n')
        f.write('import org.apache.shiro.util.CollectionUtils;\n')
        f.write('import org.mybatis.spring.SqlSessionTemplate;\n\n')
        f.write('import java.io.File;\n')
        f.write('import java.sql.Connection;\n')
        f.write('import java.sql.PreparedStatement;\n')
        f.write('import java.util.List;\n\n')
        f.write('public class ' + entity_name + 'ExcelHelper implements SqlStatement {\n\n')
        f.write('    public static long insert(String originalFilename, File dataFile, FileImport fileImport, '
                'SqlSessionTemplate sqlSessionTemplate) throws Exception {\n\n')
        f.write('        while(WorkConfig.getDataImportIsWorkingLock()) {\n')
        f.write('            //wait for other-ExcelHelper finishing the job\n        }\n')
        f.write('        WorkConfig.setDataImportIsWorkingLock(true);\n')
        f.write('        long count;\n')
        f.write('        try (SqlSession session = sqlSessionTemplate.getSqlSessionFactory().openSession();\n')
        f.write('             Connection con = session.getConnection();\n')
        f.write('             PreparedStatement ps = con.prepareStatement(INSERT_INTO_' + table_name + ')) {\n')
        f.write('            int columnsForRead = ' + columns_for_read + ';\n')
        f.write('            String yearMonth = String.format("%s%s",\n')
        f.write('                    fileImport.getYear(), fileImport.getMonth() < 10 ? '
                '"0" + fileImport.getMonth() : fileImport.getMonth());\n')
        f.write('            if (1 == fileImport.getRecover()) {\n')
        f.write('                sqlSessionTemplate.getMapper(' + entity_name + 'Dao.class).'
                'deleteByYearMonth(yearMonth);\n            }\n')
        f.write('            List<List<String>> list;\n')
        f.write('            if (originalFilename.toLowerCase().endsWith(XLSX)) {\n')
        f.write('                list = XLSXCovertCSVUtil.readXLSX(dataFile, 1, '
                '' + start_row_num + ', columnsForRead);\n')
        f.write('            } else {\n')
        f.write('                list = XLSConvertCSVUtil.readXLS(dataFile, 1, '
                '' + start_row_num + ', columnsForRead);\n')
        f.write('            }\n')
        f.write('            con.setAutoCommit(false);\n')
        f.write('            long blankRow = 0L;\n')
        f.write('            long rowsCount = 0L;\n')
        f.write('            final int commitSize = 1000;\n')
        f.write('            for (List<String> row : list) {\n')
        f.write('                if (CollectionUtils.isEmpty(row)) {\n')
        f.write('                    blankRow++;\n')
        f.write('                } else {\n')
        f.write('                    rowsCount++;\n')
        f.write('                    for (int j = 1; j < columnsForRead; j++) {\n')
        f.write('                        ps.setString(j, row.get(j));\n')
        f.write('                    }\n')
        user = int(columns_for_read) - 1
        f.write('                    ps.setString(' + str(user) + ', fileImport.getUser());\n')
        f.write('                    ps.setString(' + columns_for_read + ', yearMonth);\n')
        f.write('                    ps.addBatch();\n')
        f.write('                }\n')
        f.write('                if (rowsCount % commitSize == 0) {\n')
        f.write('                    ps.executeBatch();\n')
        f.write('                    con.commit();\n')
        f.write('                }\n')
        f.write('            }\n')
        f.write('            if (blankRow != list.size()) {\n')
        f.write('                ps.executeBatch();\n')
        f.write('                con.commit();\n')
        f.write('            }\n')
        f.write('            count = rowsCount - blankRow;\n')
        f.write('        } catch(Exception e) {\n')
        f.write('            e.printStackTrace();\n')
        f.write('            throw e;\n')
        f.write('        } finally {\n')
        f.write('            WorkConfig.setDataImportIsWorkingLock(false);\n')
        f.write('        }\n')
        f.write('        return count;\n    }\n}\n')


def create_sql(table_name, input_file='output.txt'):
    """
    生成sql文件
    :param table_name: 表名称
    :param input_file: 传入文件名
    :return:
    """
    with open('sql.txt', 'w', encoding='utf-8') as f:
        f.write('String INSERT_INTO_' + table_name.upper() + ' = "INSERT INTO ' + table_name + '(" +\n')
        with open(input_file, 'r', encoding='utf-8') as f2:
            columns = f2.readlines()
            for i in range(len(columns) - 1):
                f.write('        "' + columns[i].strip() + '," +\n')
            f.write('        "' + columns[-1].strip() + ') " +\n')
        f.write('        "VALUES(' + ('?,' * (len(columns) - 1)) + '?)";')


def create_jsp(table_name, output_file='output.txt'):
    """
    生成jsp文件
    :param table_name: 传入表名
    :param output_file: 传入字段名文件
    :return:
    """
    file_name = 'import.jsp'
    entity_name = util.up_case_first_letter(util.entity_attributes_standardize(table_name))
    with open(file_name, 'w', encoding='utf-8') as f:

        f.write('            $(\'#importBtn\').bind(\'click\', function () {  \n')
        f.write('                $(\'#file-action\').form(\'clear\');   \n')
        f.write('                $(\'#file-action\').form(\'reset\');   \n')
        f.write('                $(\'#file-action #filecontainer input\').val(\'\');\n')
        f.write('                $(\'#dataType\').val(\'' + table_name + '\');\n')
        f.write('                $(\'#import-dialog\').dialog(\'open\');\n')
        f.write('            });\n\n')
        f.write('            $(\'#import\').bind(\'click\', function () {\n')
        f.write('                var isValid = $(\'#file-action\').form(\'validate\');\n')
        f.write('                if (isValid) {\n                    $(\'#file-action\').submit();\n')
        f.write('                    $.messager.progress();\n                }\n')
        f.write('            });\n\n')
        f.write('        function ajaxFormCallback(json) {\n')
        f.write('            var isjson = Object.prototype.toString.call(json).toLowerCase() == "[object object]";\n')
        f.write('            if (isjson && json.success) {\n')
        f.write('                $(\'#import-dialog\').dialog(\'close\');\n')
        f.write('                $.messager.alert(\'消息\', json.message, \'info\');\n')
        f.write('                setTimeout(function () {\n')
        f.write('                    $(\'#dataTable\').datagrid(\'load\', {\n')
        with open(output_file, 'r', encoding='utf-8') as f2:
            columns = f2.readlines()
            for column in columns:
                column = util.entity_attributes_standardize(column.strip())
                f.write('                        ' + column + ': $(\'#' + column + '\').val(),\n')
        f.write('                    });\n                }, 2);\n')
        f.write('            } else {\n')
        f.write('                $.messager.alert(\'错误\', json.message, \'error\');\n            }\n')
        f.write('            $.messager.progress(\'close\');\n        }\n\n')
        f.write('        <a id="importBtn" href="javascript:void(0)" class="easyui-linkbutton" iconCls="icon-add" '
                'plain="true">导入</a>\n\n')
        f.write('    <div id="import-dialog" class="easyui-dialog"\n')
        f.write('         title="Excel导入"\n')
        f.write('         buttons="#import-tools"\n')
        f.write('         closed="true"\n')
        f.write('         cache="false"\n')
        f.write('         style="width:450px; height:300px"\n')
        f.write('         iconCls="icon-edit"\n')
        f.write('         modal="true">\n')
        f.write('        <iframe id="file-target" name="file-target" style="display: none"></iframe>\n')
        f.write('        <div class="modal-body">\n')
        f.write('            <form action="${ctx}/file/multipart.json" id="file-action" method="post" '
                'enctype="multipart/form-data"\n')
        f.write('                  class="form-horizontal" target="file-target">\n')
        f.write('                <input name="user" type="hidden" value="${login_name}"/>\n')
        f.write('                <div class="control-group">\n')
        f.write('                    <label class="control-label">是否覆盖：</label>\n')
        f.write('                    <div class="controls">\n')
        f.write('                        <select id="recover" name="recover" class="easyui-combobox" '
                'style="width:150px;"\n')
        f.write('                                required="required">\n')
        f.write('                            <option value="0">否</option>\n')
        f.write('                            <option value="1">是</option>\n')
        f.write('                        </select>\n')
        f.write('                    </div>\n                </div>\n')
        f.write('                <div class="control-group" style="display:none">\n')
        f.write('                    <label class="control-label">数据类型：</label>\n')
        f.write('                    <div class="controls">\n')
        f.write('                        <input id="dataType" name="dataType" class="easyui-textbox" '
                'style="width:150px;" type="text"/>\n')
        f.write('                    </div>\n                </div>\n')
        f.write('                <div class="control-group">\n')
        f.write('                    <label class="control-label">年份：</label>\n')
        f.write('                    <div class="controls">\n')
        f.write('                        <select class="easyui-combobox" name="year" style="width:150px;" '
                'required="required">\n')
        f.write('                            <c:forEach items="${years}" var="d">\n')
        f.write('                                <option value="${d}">${d}年</option>\n')
        f.write('                            </c:forEach>\n')
        f.write('                        </select>\n')
        f.write('                    </div>\n')
        f.write('                </div>\n')
        f.write('                <div class="control-group">\n')
        f.write('                    <label class="control-label">月份：</label>\n')
        f.write('                    <div class="controls">\n')
        f.write('                        <select class="easyui-combobox" name="month" style="width:150px;" '
                'required="required">\n')
        f.write('                            <c:forEach items="1,2,3,4,5,6,7,8,9,10,11,12" var="m" step="1">\n')
        f.write('                                <option value="${m}">${m}月</option>\n')
        f.write('                            </c:forEach>\n')
        f.write('                            <option value="13">全年</option>\n')
        f.write('                        </select>\n')
        f.write('                    </div>\n')
        f.write('                </div>\n')
        f.write('                <div class="control-group">\n')
        f.write('                    <label class="control-label">数据文件：</label>\n')
        f.write('                    <div class="controls">\n')
        f.write('                        <input name="file" type="file" style="width:200px" required="required"\n')
        f.write('                               value="选择..."/>\n')
        f.write('                    </div>\n')
        f.write('                </div>\n')
        f.write('            </form>\n')
        f.write('        </div>\n    </div>\n')
        f.write('    <div id="import-tools">\n')
        f.write('        <a id="import" href="javascript:void(0)" class="easyui-linkbutton" '
                'iconCls="icon-save">保存</a>\n')
        f.write('        <a href="javascript:void(0)" class="easyui-linkbutton" iconCls="icon-cancel"\n')
        f.write('           onclick="javascript:$(\'#importDialog\').dialog(\'close\')">关闭</a>\n')
        f.write('    </div>\n\n')
        f.write('    void deleteByYearMonth(@Param("yearMonth") String yearMonth);\n\n')
        f.write('    <delete id="deleteByYearMonth" parameterType="java.lang.String">\n')
        f.write('        DELETE FROM' + table_name + 'WHERE YEAR_MONTH = #{yearMonth, jdbcType = VARCHAR}\n')
        f.write('    </delete>\n\n')
        f.write('							case ' + table_name + ':\n')
        f.write('								count = ' + entity_name + 'ExcelHelper.insert(originalFilename, file, '
                'fileImport, sqlSessionTemplate);\n')
        f.write('								break;\n')


if __name__ == '__main__':
    reader_import('PatientDetailData', 19, 2)
    create_sql('PATIENT_DETAIL_DATA')
