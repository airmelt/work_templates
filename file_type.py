#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 使用魔数(magic number)检查文件类型
@file_name: file_type.py
@project: work
@version: 1.0
@date: 2019/11/21 13:45
@author: air
"""

import struct


def bytes2hex(b):
    """
    字节码转16进制字符串
    :param b: 传入字节码
    :return: 
    """
    num = len(b)
    hexstr = u""
    for i in range(num):
        t = u"%x" % b[i]
        if len(t) % 2:
            hexstr += u"0"
        hexstr += t
    return hexstr.upper()


def file_type(file_name):
    """
    获取文件类型
    :param file_name: 传入文件名称
    :return: 
    """
    binfile = open(file_name, 'rb')
    binfile.seek(0)
    hb = struct.unpack_from("B" * 8, binfile.read(8))
    filecode = bytes2hex(hb)
    print(filecode)


if __name__ == '__main__':
    # file_type("201810特殊病种.xls")
    # file_type("特殊病种test.xls")
    # file_type("居民特殊病种test.xls")
    file_type("null-张春英-010广州市妇婴医院(医保局反馈汇总20180702)(成功).xlsx")
    file_type("广州市妇女儿童医疗中心(6月份审核反馈).xlsx")

# result
# 0900040002001000
# D0CF11E0A1B11AE1
# D0CF11E0A1B11AE1
# 504B030414000600

# 常见文件格式                       文件头(十六进制)
# JPEG (jpg)                        FFD8FF
# PNG (png)                         89504E47
# GIF (gif)                         47494638
# TIFF (tif)                        49492A00
# Windows
#   Bitmap (bmp)                    424D
#   CAD (dwg)                       41433130
#   Adobe Photoshop (psd)           38425053
#   Rich Text Format (rtf)          7B5C727466
#   XML (xml)                       3C3F786D6C
#   HTML (html)                     68746D6C3E
#   Email [thorough only] (eml)     44656C69766572792D646174653A
#   Outlook Express (dbx)           CFAD12FEC5FD746F
#   Outlook (pst)                   2142444E
#   MS Word/Excel (xls.or.doc)      D0CF11E0
#   MS Access (mdb)                 5374616E64617264204A
