#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 新建导出文件/create file for exporting excel
@file_name: create_export.py
@project: work
@version: 2.0
@date: 2019/1/11 13:45
@author: air
"""

__author__ = 'air'

import util


def controller_export(entity_name, output_file='controller_export.java'):
    """
    创建Controller层export方法
    :param entity_name: 传入实体类名称
    :param output_file: 传出的Controller层方法文件
    :return:
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('    @RequestMapping(value="/export.json",method=RequestMethod.POST)\n')
        f.write('    public void export(HttpServletRequest request,HttpServletResponse response) {\n')
        f.write('       ' + entity_name[0].lower() + entity_name[1:] + 'Service.export')
        f.write(entity_name + '(request, response);\n    }\n')


def service_export(table_comment, entity_name, package_name='medicare', input_file='output.txt', comment_file = 'comment.txt'):
    """
    创建Service层导出文件
    :param table_comment: 导出的文件名
    :param entity_name: 传入实体类名称
    :param package_name: 实体类的包名
    :param input_file: 传入数据库字段名称txt文件
    :param comment_file: 传入的字段注释txt文件
    :return:
    """
    output_file = entity_name + 'Service.java'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('package com.yibo.modules.' + package_name + '.service;\n\n')
        f.write('import com.yibo.core.common.service.CrudService;\n')
        f.write('import com.yibo.core.common.utils.WebUtil;\n')
        f.write('import com.yibo.core.common.utils.excel.XSSFWriteExt;\n')
        f.write('import org.apache.commons.collections.CollectionUtils;\n')
        f.write('import org.springframework.beans.factory.annotation.Autowired;\n')
        f.write('import org.springframework.stereotype.Service;\n')
        f.write('import org.springframework.transaction.annotation.Transactional;\n')
        f.write('import com.yibo.modules.' + package_name + '.entity.' + entity_name + ';\n')
        f.write('import com.yibo.modules.' + package_name + '.dao.' + entity_name + 'Dao;\n')
        f.write('import org.springframework.util.FileCopyUtils;\n\n')
        f.write('import javax.servlet.http.HttpServletRequest;\n')
        f.write('import javax.servlet.http.HttpServletResponse;\n')
        f.write('import java.io.File;\n')
        f.write('import java.io.FileInputStream;\n')
        f.write('import java.io.PrintWriter;\n')
        f.write('import java.net.URLEncoder;\n')
        f.write('import java.sql.SQLException;\n')
        f.write('import java.util.ArrayList;\n')
        f.write('import java.util.Date;\n')
        f.write('import java.util.List;\n')
        f.write('import java.util.Map;\n\n\n')
        f.write('@Service\n')
        f.write('@Transactional(readOnly = true)\n')
        f.write('public class ' + entity_name + 'Service extends CrudService'
                                                '<' + entity_name + 'Dao, ' + entity_name + '> {\n\n')
        f.write('    @Autowired\n')
        f.write('    private ' + entity_name + 'Dao dao;\n\n')
        f.write('    private List<List<Object>> getExport() throws SQLException {\n')
        f.write('        return export();\n    }\n\n')
        f.write('    private List<List<Object>> export() throws SQLException {\n')
        f.write('        List<List<Object>> data = new ArrayList<>();\n')
        f.write('        // 获取传过来的查询参数\n')
        f.write('        Map<String,Object> paramMap = WebUtil.getAllParameters();\n')
        f.write('        List<' + entity_name + '> list = dao.getExport(paramMap);\n')
        f.write('        if (list.size() > 0) {\n')
        f.write('            for (' + entity_name + ' entity : list) {\n')
        f.write('                List<Object> objList = new ArrayList<>();\n')
        with open(input_file, 'r', encoding='utf-8') as f2:
            item = f2.readline().strip().title().replace('_', '')
            while item:
                f.write('                objList.add(entity.get' + item + '());\n')
                item = f2.readline().strip().title().replace('_', '')
        f.write('                data.add(objList);\n')
        f.write('            }\n        }\n        return data;\n    }\n\n')
        f.write('    public void export' + entity_name +
                '(HttpServletRequest request,HttpServletResponse response) {\n')
        f.write('        WebUtil.setRequest(request);\n')
        f.write('        // 创建一个文本输出流对象\n')
        f.write('        PrintWriter writer = null;\n')
        f.write('        try {\n')
        f.write('            writer = response.getWriter();\n')
        f.write('            List<String> header = new ArrayList<>();\n')
        with open(comment_file, 'r', encoding='utf-8') as f2:
            header = f2.readline().strip()
            while header:
                f.write('            header.add("' + header + '");\n')
                header = f2.readline().strip()
        f.write('            boolean pass = true;\n\n')
        f.write('            List<List<Object>> data = getExport();\n')
        f.write('            if (CollectionUtils.isEmpty(data)) {\n')
        f.write('                pass = false;\n')
        f.write('                writer.print("没有符合查询条件的数据.");\n            }\n')
        f.write('            if (pass) {\n')
        f.write('                String path = WebUtil.getRequest().getSession().'
                'getServletContext().getRealPath("data");\n')
        f.write('                String fileName = path+"/"+System.currentTimeMillis()+".xlsx";\n')
        f.write('                XSSFWriteExt.writeToExcel(data, fileName, header);\n')
        f.write('                long fileLength;\n')
        f.write('                File file = new File(fileName);\n\n')
        f.write('                String fileDisplay = "' + table_comment + '_"+new Date().getTime();\n')
        f.write('                String agent = request.getHeader("User-Agent").toUpperCase();\n')
        f.write('                if (agent.indexOf("MSIE") > 0 || (agent.indexOf("GECKO") > 0 && '
                'agent.indexOf("RV:11") > 0)) {\n')
        f.write('                    fileDisplay = URLEncoder.encode(fileDisplay, "UTF-8");\n')
        f.write('                } else {\n')
        f.write('                    fileDisplay = new String(fileDisplay.getBytes("UTF-8"), "ISO8859-1");\n')
        f.write('                }\n                fileLength = file.length();\n')
        f.write('                response.reset();\n')
        f.write('                response.setContentType("application/x-msdownload");\n')
        f.write('                response.setHeader("Content-disposition", "attachment;'
                'filename=\\""+ fileDisplay+".xlsx\\";target=_blank");\n')
        f.write('                response.setHeader("Content-Length",String.valueOf(fileLength));\n')
        f.write('                FileCopyUtils.copy(new FileInputStream(file),response.getOutputStream());\n')
        f.write('            }\n        } catch(Exception e) {\n')
        f.write('            if (null != writer) {\n')
        f.write('                response.setContentType("text/html;charset=UTF-8");\n')
        f.write('                writer.print("下载文件时发生错误.");\n')
        f.write('            }\n        }\n    }\n}\n')


def dao_export(entity_name, package_name='medicare'):
    """
    创建dao层导出文件
    :param entity_name: 传入实体类名称
    :param package_name: 实体类的包名
    :return:
    """
    output_file = entity_name + 'Dao.java'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('package com.yibo.modules.' + package_name + '.dao;\n\n')
        f.write('import com.yibo.core.common.persistence.CrudDao;\n')
        f.write('import com.yibo.modules.' + package_name + '.entity.' + entity_name + ';\n')
        f.write('import com.yibo.core.common.persistence.annotation.MyBatisDao;\n\n')
        f.write('import java.sql.SQLException;\n')
        f.write('import java.util.List;\n')
        f.write('import java.util.Map;\n\n')
        f.write('@MyBatisDao\n')
        f.write('public interface ' + entity_name + 'Dao extends CrudDao<' + entity_name + '> {\n')
        f.write('    List<' + entity_name + '> getExport(Map map)throws SQLException;\n}\n')


def xml_export(table_name, input_file='output.txt', output_file='export_xml.txt'):
    """
    创建xml语句
    :param table_name: 传入表名称 驼峰式命名/下划线命名
    :param input_file: 传入数据库字段名称txt文件
    :param output_file: 输出xml文件
    :return:
    """
    table_name = util.table_name_standardize(table_name)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('    <select id="getExport" parameterType="Map" resultMap="BaseResultMap">\n')
        f.write('        SELECT <include refid="sql" /> FROM ' + table_name + '\n')
        f.write('        <where>\n')
        f.write('            <if test="pkId != null and pkId != \'\'">\n')
        f.write('                ' + table_name + '.PK_ID = #{pkId,jdbcType=INTEGER}\n')
        f.write('            </if>\n')
        with open(input_file, 'r', encoding='utf-8') as f2:
            column = f2.readline().strip()
            attribute = util.entity_attributes_standardize(column)
            while column:
                f.write('            <if test="' + attribute + ' != null and ' + attribute + ' != \'\'">\n')
                f.write('                AND ' + table_name + '.' + column + ' LIKE \'%\' + #{'
                        + attribute + ',jdbcType=VARCHAR} + \'%\'\n')
                f.write('            </if>\n')
                column = f2.readline().strip()
                attribute = util.entity_attributes_standardize(column)
        f.write('        </where>\n')
        f.write('        order by ' + table_name + '.PK_ID\n    </select>\n')


def jsp_export(entity_name, package_name='medicare', input_file='output.txt', ):
    """
    jsp导出
    :param entity_name: 传入实体类名称
    :param package_name: 实体类的包名
    :param input_file: 传入数据库字段名称txt文件
    :return:
    """
    entity_name = util.low_case_first_letter(entity_name)
    with open(entity_name + 'Export.jsp', 'w', encoding='utf-8') as f:
        f.write('            //数据导出功能\n')
        f.write('            $(\'#exportBtn\').click(function () {\n')
        with open(input_file, 'r', encoding='utf-8') as f2:
            column = util.entity_attributes_standardize(f2.readline().strip())
            while column:
                f.write('               $(\'#export input[name="' + column +
                        '"]\').val($.trim($("#dataTableBar #' + column + '").val()));\n')
                column = util.entity_attributes_standardize(f2.readline().strip())
        f.write('               $("#export").submit();\n')
        f.write('            });\n\n')
        f.write('    <form id="export" enctype="application/x-www-form-urlencoded" method="post" style="display: none" '
                'target="_blank" action="${ctx}/' + package_name + '/' + entity_name + '/export.json">\n')
        with open(input_file, 'r', encoding='utf-8') as f2:
            column = util.entity_attributes_standardize(f2.readline().strip())
            while column:
                f.write('        <input name="' + column + '">\n')
                column = util.entity_attributes_standardize(f2.readline().strip())
        f.write('    </form>\n\n')
        f.write('            <a id="exportBtn" href="javascript:void(0)" class="easyui-linkbutton" '
                'iconCls="icon-save" plain="true">数据导出</a>')


if __name__ == '__main__':
    controller_export('明细数据', 'Home')
    # service_export('FactDiseaseipHis')
    # dao_export('FactDiseaseipHis')
    # xml_export('FactDiseaseipHis')
