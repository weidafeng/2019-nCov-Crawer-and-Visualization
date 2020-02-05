#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:           wdf
# datetime:         2/5/2020 11:52 AM
# software:         PyCharm
# project name:     2019-nCov-Crawer-and-Visualization 
# file name:        pymongo-存储文件
# description:      
# usage:            


# 获取数据库中gridfs存储的文件

from pymongo import MongoClient
import gridfs  # 安装pymongo默认安装了该库

# 链接数据库
conn = MongoClient('localhost', 27017)
db = conn['wdf_files']

# 因为MongoDB存储大文件会分为两个集合（files, chuncks), 所以还需要
fs = gridfs.GridFS(db)  # 自动获取指定数据库中存储大文件的对象

files = fs.find()  # 所有文件的游标
print(files.count())  # 1 表示只有一个文件
print(files)          # <gridfs.grid_file.GridOutCursor object at 0x000002664DC265C0>
for file in files:
    print(file.filename)     # wake.mp3

# 从数据库下载文件

for file in fs.find():
    if file.filename == 'Wake.mp3':
        with open(file.filename, 'wb') as f:  # 把数据下载的当前路径
            while True:
                # file 的 read() 函数可以获取文件内容
                data = file.read(512)  # 每次读取512字节
                if not data:
                    break
                f.write(data)

conn.close()





