#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:           wdf
# datetime:         2/5/2020 10:44 AM
# software:         PyCharm
# project name:     2019-nCov-Crawer-and-Visualization 
# file name:        pymongo-索引和聚合操作
# description:      
# usage:            

'''
MongoDB命令行操作


1、查看集合索引
db.col.getIndexes()

2、查看集合索引大小
db.col.totalIndexSize()

3、删除集合所有索引
db.col.dropIndexes()

4、删除集合指定索引
db.col.dropIndex("索引名称")


# 查看索引——默认有一个以_id为key的索引
# _id 是创建表的时候自动创建的索引，此索引是不能够删除的。
> db.wdf_class.getIndexes()
[
        {
                "v" : 2,
                "key" : {
                        "_id" : 1
                },
                "name" : "_id_",
                "ns" : "2019-nCov.wdf_class"
        }
]
>

# 创建索引
在字段age 上创建索引，1(升序);-1(降序)：
db.users.ensureIndex({age:1})

当系统已有大量数据时，创建索引就是个非常耗时的活，我们可以在后台执行，只需指定“backgroud:true”即可。
db.t3.ensureIndex({age:1} , {backgroud:true})

'''

from pymongo import MongoClient

# 链接数据库
conn = MongoClient('localhost', 27017)
db = conn['2019-nCov']
my_set = db.wdf_class


def ensure_index():
    '''注意，ensure_index被弃用了，应该使用creat_index'''

    # 以'name'字段创建索引（返回值为索引的名称）
    index = my_set.ensure_index('name')
    # 查看索引的名字: name_1
    print(index)
    # 创建符合索引
    # 输入为list包含多个元组[(), ()]

    # 如 创建name和king的复合索引
    # name升序，king降序
    index_2 = my_set.ensure_index([('name', 1), ('King', -1)])
    print(index_2)  # name_1_King_-1
    '''
    mongodb查看索引
    > db.wdf_class.getIndexes()
    [
            {
                    "v" : 2,
                    "key" : {
                            "_id" : 1
                    },
                    "name" : "_id_",
                    "ns" : "2019-nCov.wdf_class"
            },
            {
                    "v" : 2,
                    "key" : {
                            "name" : 1
                    },
                    "name" : "name_1",
                    "ns" : "2019-nCov.wdf_class"
            },
            {
                    "v" : 2,
                    "key" : {
                            "name" : 1,
                            "King" : -1
                    },
                    "name" : "name_1_King_-1",
                    "ns" : "2019-nCov.wdf_class"
            }
    ]
    >
    '''

    # 查看所有索引
    print(my_set.index_information())
    # {'_id_': {'v': 2, 'key': [('_id', 1)], 'ns': '2019-nCov.wdf_class'}, 'name_1': {'v': 2, 'key': [('name', 1)], 'ns': '2019-nCov.wdf_class'}, 'name_-1': {'v': 2, 'key': [('name', -1.0)], 'ns': '2019-nCov.wdf_class'}}
    for i in my_set.list_indexes():
        print(i)

    # # 创建唯一索引——要求索引key未创建过，否则报错重复DuplicateKeyError
    # index_3 = my_set.ensure_index('name', unique=True)
    # print(index_3)
    # # 创建稀疏索引  sparse=True

    # 删除索引
    print(my_set.drop_index('name_1_King_-1'))  # 删除指定索引，输入索引名（而非域名）
    print(my_set.drop_indexes())  # 删除所有索引（除了_id)

    print('delete all indexes')
    # 重新查看——不为空，还有_id索引
    for i in my_set.list_indexes():
        print(i)


def create_indexes():
    # 同时创建多个索引
    from pymongo import IndexModel

    # 第一个是复合索引
    index_1 = IndexModel([('name', 1), ('King', -1)])
    # 第二个索引
    index_2 = IndexModel([('King_name', 1)])

    # 同时创建
    indexes = my_set.create_indexes([index_1, index_2])

    # 查看索引
    for i in my_set.list_indexes():
        print(i)

    # 删除所有索引
    my_set.drop_indexes()


def aggregate_db():
    # 聚合操作， 与mongo shell语法一致
    # 返回值： 迭代器，与find的返回值一致

    # 可以先写外面写聚合管道（字典）， 更美观
    l = [{'$group': {'_id': '$King',
                     'count': {'$sum': 1}}},  # 第一个，查找$king字段的数据，赋值给_id（可以任取），并按该索引计数，赋值给count
         {'$match': {'count': {'$gt': 1}}}    # 第二个，查找count数大于1的数据
         ]

    cursor = my_set.aggregate(l)
    for c in cursor:
        print(c)

    '''
    {'_id': '雍正', 'count': 2}
    {'_id': '康熙', 'count': 2}   
    '''

def main():
    # ensure_index()

    # create_indexes()

    aggregate_db()

if __name__ == '__main__':
    main()
