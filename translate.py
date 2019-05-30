#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: 调用谷歌翻译excel并保存为txt
source:
    https://blog.csdn.net/xc_zhou/article/details/81009835?utm_source=blogxgwz3
    https://www.jianshu.com/p/95cf6e73d6ee
@file_name: translate.py
@project: work
@version: 1.0
@date: 2019/1/11 13:45
@author: air
"""

__author__ = 'air'

import urllib.request
from bs4 import BeautifulSoup
import re
import pandas as pd
import execjs
from time import sleep


class Py4Js:
    """
    执行js代码类
    """
    def __init__(self):
        """
        编译js代码
        """
        self.ctx = execjs.compile(""" 
        var b = function (a, b) {
            for (var d = 0; d < b.length - 2; d += 3) {
                var c = b.charAt(d + 2),
                    c = "a" <= c ? c.charCodeAt(0) - 87 : Number(c),
                    c = "+" == b.charAt(d + 1) ? a >>> c : a << c;
                a = "+" == b.charAt(d) ? a + c & 4294967295 : a ^ c
            }
            return a
        };
    
        var tk =  function (a, TKK) {
            for (var e = TKK.split("."), h = Number(e[0]) || 0, g = [], d = 0, f = 0; f < a.length; f++) {
                var c = a.charCodeAt(f);
                128 > c ? g[d++] = c : (2048 > c ? g[d++] = c >> 6 | 192 : (55296 == (c & 64512) && f + 1 < a.length && 56320 == (a.charCodeAt(f + 1) & 64512) ? (c = 65536 + ((c & 1023) << 10) + (a.charCodeAt(++f) & 1023), g[d++] = c >> 18 | 240, g[d++] = c >> 12 & 63 | 128) : g[d++] = c >> 12 | 224, g[d++] = c >> 6 & 63 | 128), g[d++] = c & 63 | 128)
            }
            a = h;
            for (d = 0; d < g.length; d++) a += g[d], a = b(a, "+-a^+6");
            a = b(a, "+-3^+b+-f");
            a ^= Number(e[1]) || 0;
            0 > a && (a = (a & 2147483647) + 2147483648);
            a %= 1E6;
            return a.toString() + "." + (a ^ h);
        }
     """)

    def get_tk(self, text, a_tkk):
        """
        获取tk值
        :param text:
        :param a_tkk: tkk值
        :return: tk值
        """
        return self.ctx.call("tk", text, a_tkk)


def build_url(text, tk):
    """
    获取url, tk动态变化
    :param text: 传入的要翻译的文本
    :param tk: 动态变化的tk值
    :return: url
    """
    base_url = 'https://translate.google.cn/translate_a/single'
    base_url += '?client=webapp&'
    base_url += 'sl=zh-CN&'
    base_url += 'tl=en&'
    base_url += 'hl=zh-CN&'
    base_url += 'dt=at&'
    base_url += 'dt=bd&'
    base_url += 'dt=ex&'
    base_url += 'dt=ld&'
    base_url += 'dt=md&'
    base_url += 'dt=qca&'
    base_url += 'dt=rw&'
    base_url += 'dt=rm&'
    base_url += 'dt=ss&'
    base_url += 'dt=t&'
    base_url += 'source=bh&'
    base_url += 'ssel=3&'
    base_url += 'tsel=3&'
    base_url += 'kc=1&'
    base_url += 'tk=' + str(tk) + '&'
    base_url += 'q=' + urllib.parse.quote(text)
    return base_url


def get_tkk():
    """
    获取tkk, 用来解析tk值
    :return: tkk值
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    url = 'https://translate.google.com/'
    req = urllib.request.Request(url, None, headers, None, False)
    response = urllib.request.urlopen(req)
    soup = BeautifulSoup(response.read(), 'lxml')
    tkk_result = re.search('tkk:\'(.*?)\',', str(soup)).group(1)
    return tkk_result


def translate(text):
    """
    翻译文本
    :param text: 传入翻译文本
    :return: 翻译结果
    """
    text_tkk = get_tkk()
    headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8'
            }
    js = Py4Js()
    url = build_url(text, js.get_tk(text, text_tkk))
    req = urllib.request.Request(url, None, headers, None, False)
    response = urllib.request.urlopen(req)
    soup = BeautifulSoup(response.read(), 'lxml')
    result = soup.find('p').string
    translated_text = re.search('\[\[\["(.*?)"', result).group(1)
    return translated_text


def excel2txt(input_file, row=0, begin_column=0, output_file='output.txt'):
    """
    将excel的表格中的表头提取, 并转化成txt, 每一行即一个单元格的翻译结果
    :param input_file: 传入excel文件名
    :param row: 读取的表头的行数, 默认为0
    :param begin_column: 开始的列数, 默认为0
    :param output_file: 生成的txt文件名
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
            item = translate(item).upper()
            item = item.replace(' ', '_')
            print(item)
            sleep(1)
            f.write(item + '\n')


def txt2txt(input_file="comment.txt", output_file='output.txt'):
    """
    将传入的文件提取, 并转化成txt, 每一行对应一个翻译结果
    :param input_file: 传入txt文件名
    :param output_file: 生成的txt文件名
    :return:
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        text_list = f.readlines()
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in text_list:
            item = ''.join(item.split())
            item = translate(item).upper()
            item = item.replace(' ', '_')
            print(item)
            sleep(1)
            f.write(item + '\n')


if __name__ == '__main__':
    excel2txt(r'201802月新版居民.xls', 3, 1, 'output2.txt')
