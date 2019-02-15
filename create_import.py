#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 新建导入文件
@file_name: create_import.py
@project: work_templates
@version: 1.0
@date: 2019/1/11 23:05
@author: air
"""
import util

__author__ = 'air'


def reader_import(entity_name, columns_for_read, start_row_num):
    columns_for_read = str(columns_for_read)
    start_row_num = str(start_row_num)
    table_name = util.table_name_standardize(entity_name)
    with open(entity_name + 'ExcelHelper.java', 'w', encoding='utf-8') as f:
        f.write('package com.yibo.modules.medicare.reader;\n\n')
        f.write('import com.yibo.core.common.utils.excel.XLSConvertCSVUtil;\n')
        f.write('import com.yibo.core.common.utils.excel.XLSXCovertCSVUtil;\n')
        f.write('import com.yibo.modules.medicare.dao.' + entity_name + 'Dao;\n')
        f.write('import com.yibo.modules.medicare.entity.FileImport;\n')
        f.write('import com.yibo.modules.medicare.others.WorkConfig;\n')
        f.write('import com.yibo.modules.medicare.reader.SqlStatement;\n')
        f.write('import org.apache.ibatis.session.SqlSession;\n')
        f.write('import org.apache.shiro.util.CollectionUtils;\n')
        f.write('import org.mybatis.spring.SqlSessionTemplate;\n\n')
        f.write('import java.io.File;\n')
        f.write('import java.sql.Connection;\n')
        f.write('import java.sql.PreparedStatement;\n')
        f.write('import java.util.List;\n')
        f.write('import java.util.Map;\n')
        f.write('public class ' + entity_name + 'ExcelHelper  implements SqlStatement {\n\n')
        f.write('    public static long insert(String originalFilename, File dataFile, FileImport fileImport, '
                'SqlSessionTemplate sqlSessionTemplate) throws Exception {\n\n')
        f.write('        while(WorkConfig.getDataImportIsWorkingLock()) {\n')
        f.write('            //wait for other-ExcelHelper finishing the job\n        }\n')
        f.write('        WorkConfig.setDataImportIsWorkingLock(true);\n')
        f.write('        Long count;\n')
        f.write('        SqlSession session = null;\n')
        f.write('        Connection con = null;\n')
        f.write('        PreparedStatement ps = null;\n')
        f.write('        try {\n')
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
        f.write('            session = sqlSessionTemplate.getSqlSessionFactory().openSession();\n')
        f.write('            con = session.getConnection();\n')
        f.write('            con.setAutoCommit(false);\n')
        f.write('            ps = con.prepareStatement(INSERT_INTO_' + table_name + ');\n')
        f.write('            int blankRow = 0;\n')
        f.write('            int rowsCount = 0;\n')
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
        f.write('            ' + entity_name + 'Dao dao = sqlSessionTemplate.getMapper(' + entity_name + 'Dao.class);\n')
        f.write('            Map<String,Object> blankRowMap = dao.selectClearInvalidDataCount();\n')
        f.write('            blankRow += Integer.parseInt(blankRowMap.get("blankRow").toString());\n')
        f.write('            count = new Long(rowsCount - blankRow);\n')
        f.write('            dao.clearInvalidData();\n')
        f.write('        } catch(Exception e) {\n')
        f.write('            throw e;\n')
        f.write('        } finally {\n')
        f.write('            if (ps != null) {\n')
        f.write('                ps.close();\n')
        f.write('            }\n')
        f.write('            if (con != null) {\n')
        f.write('                con.close();\n')
        f.write('            }\n')
        f.write('            if(session != null){\n')
        f.write('                session.close();\n')
        f.write('            }\n')
        f.write('            WorkConfig.setDataImportIsWorkingLock(false);\n')
        f.write('        }\n')
        f.write('        return count;\n    }\n}\n')


def create_sql(entity_name, input_file='output.txt'):
    table_name = util.table_name_standardize(entity_name)
    with open('sql.txt', 'w', encoding='utf-8') as f:
        f.write('String INSERT_INTO_' + table_name + ' = "INSERT INTO ' + table_name + '(" +\n')
        with open(input_file, 'r', encoding='utf-8') as f2:
            columns = f2.readlines()
            for column in columns:
                f.write('        "' + column.strip() + '," +\n')
        f.write('        "FCreateUser," +\n')
        f.write('        "FYearMonth)" +\n')
        f.write('        "values(' + ('?,' * (len(columns) + 1)) + '?)";')


if __name__ == '__main__':
    # reader_import('CountryDetailData', 29, 6)
    create_sql('INDICATOR_MANAGEMENT')
