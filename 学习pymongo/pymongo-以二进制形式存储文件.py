#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:           wdf
# datetime:         2/5/2020 12:35 PM
# software:         PyCharm
# project name:     2019-nCov-Crawer-and-Visualization 
# file name:        pymongo-以二进制形式存储文件
# description:      
# usage:


from pymongo import MongoClient
import bson.binary   # 安装pymongo自动安装bson库

conn = MongoClient('localhost', 27017)
db = conn['wdf_files']
my_set = db['wdf_image']  # 不存在则自动创建
def save_file():
    # 存储二进制文件
    ## 以二进制形式读取图片——打开
    f = open('pycharm下的MongoDB可视化插件.png', 'rb')

    ## 将读取的二进制流转化为bson格式二进制流——转换格式
    content = bson.binary.Binary(f.read())

    ## 存储到数据库——插入
    my_set.insert({'filename':'pycharm下的MongoDB可视化插件.png',
                   'data': content})

    conn.close()

    '''
    在MongoDB查看数据
    > show dbs
    2019-nCov  0.001GB
    admin      0.000GB
    config     0.000GB
    local      0.000GB
    wdf        0.000GB
    wdf_files  0.011GB
    > use wdf_files
    switched to db wdf_files
    > show tables
    fs.chunks
    fs.files
    wdf_image    # 刚刚新建的set
    > db.wdf_image.find()
    { "_id" : ObjectId("5e3a4a47e255a4eeefb275c8"), "filename" : "pycharm下的MongoDB可视化插件.png", "data" : BinData(0,"iVBORw0KGgoAAAANSUhEUgAAB4AAAAKrCAYAAAAQ8ZCUAAAACXBIWXMAABJ0AAASdAHeZh94AAAA
    '''


def fetch_files():
    # 提取文件
    files = my_set.find({'filename': 'pycharm下的MongoDB可视化插件.png'})
    # find 的返回值为cursor（迭代器），哪怕只有一项，也需要通过遍历读取
    # 如果不想遍历，可以使用find_one， 返回值是字典

    # 直接通过字典形式索引
    for file in files:
        with open('new_' + file['filename'], 'wb') as f:
            f.write(file['data'])




def main():
    # save_file()

    fetch_files()

if __name__ == '__main__':
    main()
