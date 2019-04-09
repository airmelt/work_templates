#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 新建MyBatis的xml文件/create xml file for MyBatis
@file_name: create_xml.py
@project: work_templates
@version: 1.0
@date: 2019/04/08 16:27
@author: air
"""

__author__ = 'air'

import util


def create_xml(entity_name, table_name, package_name='medicare', input_file='output.txt'):
    output_file = entity_name + '.xml'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" '
                '"http://mybatis.org/dtd/mybatis-3-mapper.dtd">\n')
        f.write('<mapper namespace="com.yibo.modules.' + package_name + '.dao.' + entity_name + 'Dao">\n\n')
        f.write('    <sql id="sql">\n')
        f.write('        ' + table_name + '.PK_ID AS ' + table_name + '_PK_ID, \n')
        with open(input_file, 'r', encoding='utf-8') as f1:
            column = f1.readline().strip()
            while column:
                f.write('        ' + table_name + '.' + column + ' AS ' + table_name + '_' + column + ', \n')
                column = f1.readline().strip()
        f.write('    </sql>\n\n')
        f.write('    <resultMap id="BaseResultMap" '
                'type="com.yibo.modules.' + package_name + '.entity.' + entity_name + '">\n')
        f.write('        <id column="' + table_name + '_PK_ID" jdbcType="BIGINT" property="pkId"/>\n')
        with open(input_file, 'r', encoding='utf-8') as f1:
            column = f1.readline().strip()
            while column:
                attribute = util.entity_attributes_standardize(column)
                f.write('        <result column="' + table_name + '_' + column +
                        '" jdbcType="VARCHAR" property="' + attribute + '"/>\n')
                column = f1.readline().strip()
        f.write('    </resultMap>\n\n')
        f.write('    <select id="findPage" parameterType="java.util.Map" resultMap="BaseResultMap">\n')
        f.write('        SELECT\n')
        f.write('        <include refid="sql"/>\n')
        f.write('        FROM ' + table_name + '\n')
        f.write('        <where>\n')
        f.write('            <if test="pkId != null and pkId != '' ">\n')
        f.write('                ' + table_name + '.PK_ID = #{pkId,jdbcType=VARCHAR}\n')
        f.write('            </if>\n')
        with open(input_file, 'r', encoding='utf-8') as f1:
            column = f1.readline().strip()
            while column:
                attribute = util.entity_attributes_standardize(column)
                f.write('            <if test="' + attribute + ' != null and ' + attribute + ' != '' ">\n')
                f.write('                AND ' + table_name + '.' + column +
                        ' LIKE \'%\' + #{' + attribute + ',jdbcType=VARCHAR} + \'%\'\n')
                f.write('            </if>\n')
                column = f1.readline().strip()
        f.write('        </where>\n')
        f.write('        ORDER BY ' + table_name + '.PK_ID\n')
        f.write('    </select>\n\n')
        f.write('    <delete id="delete" parameterType="java.lang.Long">\n')
        f.write('       DELETE FROM' + table_name + ' WHERE ' + table_name + '.PK_ID =  #{pkId,jdbcType=BIGINT}\n')
        f.write('    </delete>\n\n')
        f.write('    <insert id="insert" parameterType="com.yibo.modules.' +
                package_name + '.entity.' + entity_name + '">\n')
        f.write('        INSERT INTO ' + table_name + ' (\n')
        columns = []
        attributes = []
        with open(input_file, 'r', encoding='utf-8') as f1:
            column = f1.readline().strip()
            while column:
                columns.append(column)
                attributes.append(util.entity_attributes_standardize(column))
                column = f1.readline().strip()
        leng = len(columns)
        for i, x in enumerate(columns):
            if i != len(columns) - 1:
                f.write('        ' + x + ', \n')
                continue
            f.write('        ' + x + '\n')
        f.write('        )\n')
        f.write('        VALUES\n        (\n')
        for i, x in enumerate(attributes):
            if i != len(attributes) - 1:
                f.write('        #{' + x + ', jdbcType = VARCHAR}, \n')
                continue
            f.write('        #{' + x + ', jdbcType = VARCHAR}\n')
        f.write('        )\n')
        f.write('    </insert>\n\n')
        f.write('    <update id="update" parameterType="com.yibo.modules.' +
                package_name + '.entity.' + entity_name + '">\n')
        f.write('        UPDATE ' + table_name + '\n')
        f.write('        <set>\n')
        for i in range(leng - 1):
            f.write('            ' + columns[i] + ' = #{' + attributes[i] + ', jdbcType = VARCHAR}, \n')
        f.write('            ' + columns[-1] + ' = #{' + attributes[-1] + ', jdbcType = VARCHAR}\n')
        f.write('        </set>\n')
        f.write('        WHERE ' + table_name + '.PK_ID = #{pkId, jdbcType = BIGINT}\n')
        f.write('    </update>\n\n')
        f.write('    <update id="updateNull" parameterType="com.yibo.modules.' +
                package_name + '.entity.' + entity_name + '">\n')
        f.write('        UPDATE ' + table_name + '\n')
        f.write('        <set>\n')
        for i in range(leng - 1):
            f.write('            <if test="' + attributes[i] + ' != null and ' + attributes[i] + ' != \'\'">\n')
            f.write('                ' + table_name + '.' + columns[i] + ' = #{' +
                    attributes[i] + ', jdbcType = VARCHAR}, \n')
            f.write('            </if>\n')
        f.write('            <if test="' + attributes[-1] + ' != null and ' + attributes[-1] + ' != \'\'">\n')
        f.write('                ' + table_name + '.' + columns[-1] + ' = #{' +
                attributes[-1] + ', jdbcType = VARCHAR}\n')
        f.write('            </if>\n')
        f.write('        </set>\n')
        f.write('        WHERE ' + table_name + '.PK_ID = #{pkId,jdbcType=BIGINT}\n')
        f.write('    </update>\n\n')
        f.write('    <select id="queryBySql" parameterType="java.lang.String" resultType="java.util.Map">\n')
        f.write('        ${executeSql}\n')
        f.write('    </select>\n\n')
        f.write('    <delete id="deleteByIds" parameterType="java.lang.String">\n')
        f.write('        DELETE FROM ' + table_name + ' WHERE PK_ID IN\n')
        f.write('        <foreach collection="list" item="id" open="(" separator="," close=")">\n')
        f.write('            #{id}\n')
        f.write('        </foreach>\n')
        f.write('    </delete>\n\n')
        f.write('</mapper>')


if __name__ == '__main__':
    create_xml('TbDrgsDiseaseScore', 'TB_DRGS_DISEASE_SCORE', package_name='drgsdisease', input_file='output.txt')
