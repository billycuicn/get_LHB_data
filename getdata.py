#coding=utf-8
#从东方财富网中抓取龙虎榜数据
#copyright@BillyCui

import os
import re
import string

import requests
from bs4 import BeautifulSoup

import pymysql

idate = input('请输入需要导入的日期：')
url='http://data.eastmoney.com/stock/tradedetail/'+idate+'.html'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
headers = { 'User-Agent' : user_agent }
r = requests.get(url,headers=headers)   #连接
content = r.text    #获取内容，自动转码unicode

soup = BeautifulSoup(content,"lxml")
tags1 = soup.select('script')   #选取所有<Script>标签
tag1 = tags1[10]    #选取第十个<Script>标签，是我们所要的
tag1=''.join(tag1)  #把选中的便签list变成string

pat = re.compile('[[].*[]]',re.S)   #在这个string中选择[]中间的部分
result = pat.findall(tag1)

result = ''.join(result)
D_result = eval(result)


#任意字典数据，插入到MySQL数据库中
def insert(base_name, table_name, dic):
    # 连接数据库，创建游标
    db = pymysql.connect('localhost', 'username', 'password', charset='utf8', db=base_name)
    cursor = db.cursor()
    # 字典生成sql
    ls = list(dic)
    sentence = 'insert %s (' % table_name + ','.join(ls) + ') values (' +\
               ','.join(['"%({})s"'.format(field) for field in ls]) + ');'
    sentence = sentence % dic
    print(sentence)
    # 执行、提交、关闭
    try:
        cursor.execute(sentence)
        db.commit()
    except Exception as error:
        print('\033[033m%s\033[0m' % error)  # yellow
    cursor.close()
    db.close()

for result in D_result:
    insert ('mystock','t_em_lhb',result)
