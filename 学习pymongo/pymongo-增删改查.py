#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:           wdf
# datetime:         2/4/2020 9:08 PM
# software:         PyCharm
# project name:     2019-nCov-Crawer-and-Visualization 
# file name:        pymongo-增删改查
# description:      
# usage:            

'''
插入完成没有输出提示，可以在命令行查看

cmd进入控制台

# 打开mongodb数据库
mongo
# 查看所有数据库
show dbs
# 切换指定的数据库
use 2019-nCov
# 查看当前数据库的所有table
show tables
# 查看当前table的所有内容
db.wdf_class.find()  # 可以看到数据已成功插入
db.wdf_class.find({}, {_id:0})  # 不显示id字段


# MongoDB命令行与python语法的一些不同
-  true、false —— True，False
- null —— None
- $set 等操作符 —— 用 '' 引起来


########## 示例  ##########
> show dbs  # 查看所有数据库
2019-nCov  0.000GB
admin      0.000GB
config     0.000GB
local      0.000GB
wdf        0.000GB
> use 2019-nCov  # 使用指定数据库
switched to db 2019-nCov
> show tables  # 查看该数据库下的所有文档表
DXYAbroad
DXYArea
DXYNews
DXYOverall
DXYProvince
DXYRumors
wdf_class
> db.wdf_class.find()
{ "_id" : ObjectId("5e39703f626efb2104f17f19"), "name" : "张铁林", "King" : "乾隆" }
> db.wdf_class.find({},{_id:0})
{ "name" : "张铁林", "King" : "乾隆" }
{ "name" : "陈道明", "King" : "康熙" }
{ "name" : "张铁林", "King" : "康熙" }


## 查找
db.DXYProvince.find({},{'_id': 0})

> db.DXYProvince.find({},{'_id': 0, 'createTime':0, 'modifyTime':0, 'crawlTime':0, 'countryType':0, "operator" : 0, "country" :0,  "provinceId":0, "provinceName":0, 'cityName':0, 'suspectedCount':0, 'curedCount':0, 'deadCount':0})
{ "provinceShortName" : "西藏", "confirmedCount" : 1, "comment" : "" }
{ "provinceShortName" : "湖北", "confirmedCount" : 4586, "comment" : "待明确地区：治愈30" }
{ "provinceShortName" : "广东", "confirmedCount" : 354, "comment" : "待明确地区治愈2例" }
{ "provinceShortName" : "浙江", "confirmedCount" : 428, "comment" : "" }
{ "provinceShortName" : "北京", "confirmedCount" : 114, "comment" : "待明确地区：确诊3死亡1" }
{ "provinceShortName" : "上海", "confirmedCount" : 112, "comment" : "治愈数据统一归属上海市公卫临床中心，暂无具体分区" }
{ "provinceShortName" : "湖南", "confirmedCount" : 277, "comment" : "" }
{ "provinceShortName" : "安徽", "confirmedCount" : 200, "comment" : "" }
...


# 使用操作符  查找确诊人数大于400的数据
> db.DXYProvince.find({'confirmedCount': {$gt:400}},{'_id': 0, 'createTime':0, 'modifyTime':0, 'crawlTime':0, 'countryType':0, "operator" : 0, "country" :0,  "provinceId":0, "provinceName":0, 'cityName':0, 'suspectedCount':0, 'curedCount':0, 'deadCount':0})
{ "provinceShortName" : "湖北", "confirmedCount" : 4586, "comment" : "待明确地区：治愈30" }
{ "provinceShortName" : "浙江", "confirmedCount" : 428, "comment" : "" }
{ "continents" : "", "provinceShortName" : "河南", "confirmedCount" : 422, "comment" : "待明确地区：治愈1" }
{ "continents" : "", "provinceShortName" : "广东", "confirmedCount" : 520, "comment" : "" }
{ "continents" : "", "provinceShortName" : "浙江", "confirmedCount" : 599, "comment" : "" }
{ "continents" : "", "provinceShortName" : "湖北", "confirmedCount" : 7153, "comment" : "待明确地区：治愈36" }
>

## 修改
# update
> db.wdf_class.update({'name':'张铁林'},{'name':'国立'})  # 注意，如果这样修改（update(spec,document))，则会把指定条件的整条数据替换为新输入的document，而非仅仅替换指定字段
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
> db.wdf_class.find({},{_id:0} )                   立'})
{ "name" : "国立" }
{ "name" : "陈道明", "King" : "康熙" }
{ "name" : "张铁林", "King" : "康熙" }
{ "name" : "唐国强", "King" : "雍正" }
{ "name" : "陈建斌", "King" : "雍正" }
{ "name" : "郑少秋", "King" : "乾隆" }
>

# 要想修改指定字段，应该使用$set操作符
> db.wdf_class.update({'name':'郑少秋'},{$set:{'name':'少秋'}})
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
> db.wdf_class.find({},{_id:0} )                           '}})
{ "name" : "国立" }
{ "name" : "陈道明", "King" : "康熙" }
{ "name" : "张铁林", "King" : "康熙" }
{ "name" : "唐国强", "King" : "雍正" }
{ "name" : "陈建斌", "King" : "雍正" }
{ "name" : "少秋", "King" : "乾隆" }


##################################

'''

import pymongo
from pymongo import MongoClient

# 创建连接对象
conn = MongoClient(host='localhost', port=27017)

# 创建数据库对象（如果不存在，会自动创建）
db = conn['2019-nCov']

# 创建集合对象（如果不存在，会自动创建）
my_set = db['wdf_class']


# 等价于 my_set = db.wdf_class
# 实现原理为__getitem__  __setitem__ 的包装


def print_db():
    # 查看数据库
    print(db)
    '''
    Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), '2019-nCov')
    '''

    # 查看集合
    print(my_set)
    '''
    Collection(Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), '2019-nCov'), 'wdf_class')
    '''

    # 查看集合支持的函数
    print(dir(my_set))
    '''
    ['_BaseObject__codec_options', '_BaseObject__read_concern', '_BaseObject__read_preference', '_BaseObject__write_concern', '_Collection__create', '_Collection__create_index', '_Collection__database', '_Collection__find_and_modify', '_Collection__full_name', '_Collection__name', '_Collection__write_response_codec_options', '__call__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__next__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_aggregate', '_aggregate_one_result', '_command', '_count', '_delete', '_delete_retryable', '_insert', '_insert_one', '_legacy_write', '_map_reduce', '_read_preference_for', '_socket_for_reads', '_socket_for_writes', '_update', '_update_retryable', '_write_concern_for', '_write_concern_for_cmd', 
     'aggregate', 'aggregate_raw_batches', 'bulk_write', 'codec_options', 'count', 'count_documents', 'create_index', 
     'create_indexes', 'database', 'delete_many', 'delete_one', 'distinct', 'drop', 'drop_index', 'drop_indexes', 'ensure_index',
      'estimated_document_count', 'find', 'find_and_modify', 'find_one', 'find_one_and_delete', 'find_one_and_replace',
       'find_one_and_update', 'find_raw_batches', 'full_name', 'group', 'index_information', 'initialize_ordered_bulk_op', 
       'initialize_unordered_bulk_op', 'inline_map_reduce', 'insert', 'insert_many', 'insert_one', 'list_indexes', 'map_reduce',
        'name', 'next', 'options', 'parallel_scan', 'read_concern', 'read_preference', 'reindex', 'remove', 'rename', 'replace_one', 
        'save', 'update', 'update_many', 'update_one', 'watch', 'with_options', 'write_concern']
    '''


def insert_db():
    # 插入数据
    ## insert 可以插入一条数据，或者插入一个列表 —— 只用这个就可以实现以下所有插入功能
    # 插入一条数据
    # my_set.insert({'name': '张铁林', 'King': '乾隆'})
    # 一次插入多条数据
    # my_set.insert([{'name': '陈道明', 'King': '康熙'}, {'name': '张铁林', 'King': '康熙'}])

    ## insrt_many 只能插入列表（但列表可以只有一条文档）
    # my_set.insert_many([{'name': '唐国强', 'King': '雍正'}, {'name': '陈建斌', 'King': '雍正'}])

    ## insert_one 只能插入一条
    # my_set.insert_one({'name': '郑少秋', 'King': '乾隆'})

    ## save实现插入
    my_set.save({'name': '吴奇隆', 'King': '四爷'})

    ## 此外，还可以用updata实现插入——MongoDB数据库一共三种插入方法

    # 操作完成后可以关闭数据库
    conn.close()
    print('insert document to database')


def remove_db():
    # 删除数据 remove
    ## 删除指定条件的数据, 如果没有该指定条件，也不会报错
    my_set.remove({'name': '吴奇隆'}, multi=False)  # multi默认为True，表示删除所有找到的数据，False表示只删除第一条符合条件的文档

    ## 删除所有数据
    # my_set.remove()

    # 操作完成后可以关闭数据库
    conn.close()
    print('delete document from database')


def find_data():
    # find 查找数据库内容
    # 返回一个游标cursor， 可以理解为迭代器，迭代器的每个对象都是字典
    # 注意，一个迭代器只能访问一次，要想访问多次需要重新生成

    # cursor = my_set.find()  # find 里面什么都不写，表示查找所有数据
    cursor = my_set.find({}, {'_id': 0})  # 不显示id字段

    print(cursor)
    print(type(cursor))
    '''
    <pymongo.cursor.Cursor object at 0x000001478B24C470>
    <class 'pymongo.cursor.Cursor'>
    '''
    for c in cursor:
        print(type(c), c)  # 每个对象都是字典形式
        # 可以操作字典，如c['name']


def find_data_2():
    # 使用find的操作符, 与命令行下的区别在于，操作符需要用引号括起来
    """
    符号含义示例
    $lt小于{'age': {'$lt': 20}}
    $gt大于{'age': {'$gt': 20}}
    $lte小于等于{'age': {'$lte': 20}}
    $gte大于等于{'age': {'$gte': 20}}
    $ne不等于{'age': {'$ne': 20}}
    $in在范围内{'age': {'$in': [20, 23]}}
    $nin不在范围内{'age': {'$nin': [20, 23]}}
    $exists存在某个字段{'gender': {'$exists': True}  # 找出所有存在gender字段的数据

    其他符号含义示例示例含义
    $regex匹配正则{'name': {'$regex': '^M.*'}}name以M开头
    $exists属性是否存在{'name': {'$exists': True}}name属性存在
    $type类型判断{'age': {'$type': 'int'}}age的类型为int
    $mod数字模操作{'age': {'$mod': [5, 0]}}年龄模5余0
    $text文本查询{'$text': {'$search': 'Mike'}}text类型的属性中包含Mike字符串
    $where高级条件查询{'$where': 'obj.fans_count == obj.follows_count'}自身粉丝数等于关注数
    """
    # 这些操作的更详细用法在可以在MongoDB官方文档找到：
    # https://docs.mongodb.com/manual/reference/operator/query/

    # 切换之前的丁香园数据库
    my_set = db.DXYProvince

    # 使用操作符（在第一个域）
    cursor = my_set.find({'confirmedCount': {'$gt': 400}}, {'_id': 0, 'createTime': 0, 'modifyTime': 0, 'crawlTime': 0,
                                                            'countryType': 0, "operator": 0, "country": 0,
                                                            "provinceId": 0, "provinceName": 0, 'cityName': 0,
                                                            'suspectedCount': 0, 'curedCount': 0, 'deadCount': 0})
    # for c in cursor:
    #     print(c)

    print('*********************************')
    # 游标对象的几个方法
    # next
    # count()  # 计数
    # limit(3) # 只访问三条数据
    # skip(2)  # 跳过前两条，从第三条开始访问
    # sort('age', pymongo.ASCENDING)  # 以age字段，升序排序  —— 单个排序条件
    # sort([('age', 1), ('name', -1)])  # 第一条件为age升序，第二条件为姓名降序
    # 等
    print(cursor.next)
    print(cursor.count())
    # for i in cursor.skip(2).limit(3):
    #     print(i)

    for i in cursor.sort('confirmedCount', pymongo.DESCENDING):  # ascending = 1
        print(i)
    print('*********************************')

    # 1. 查找范围： 确诊数少于10
    # 2. 设置显示字段
    # 3. 排序, 确诊数降序，省份id升序
    for i in my_set.find({'confirmedCount': {'$lt': 10}},
                         {'_id': 0, 'confirmedCount': 1, 'provinceId': 1, 'provinceShortName': 1,
                          'suspectedCount': 1}).sort([('confirmedCount', -1), ('provinceId', 1)]):
        print(i)

    print('*********************************')

    # 也可以把条件写到外面，赋值进去（更美观）
    find_cond = {'confirmedCount': {'$lt': 10}}
    show_cond = {'_id': 0, 'confirmedCount': 1, 'provinceId': 1, 'provinceShortName': 1, 'suspectedCount': 1}
    sort_cond = [('confirmedCount', -1), ('provinceId', 1)]
    for i in my_set.find(find_cond, show_cond).sort(sort_cond):
        print(i)


def find_one():
    # 返回值为字典形式，查找到的第一条符合条件的数据
    my_set = db['DXYProvince']
    filter = {'$and': [{'confirmedCount': {'$gt': 10}}, {'deadCount': {'$gt': 1}}]}
    print(my_set.find_one(filter))


def update_db():
    # update 更新数据
    my_set = db['wdf_class']

    # 注意document的写法，没有使用操作符，则会把name=张国立整条数据替换为name=国立，其他字段删除
    # my_set.update(spec={'name': '张国立'}, document={'name': '国立'})

    # 要想仅修改指定字段，其他字段保留不变，应该使用 $set 操作符
    my_set.update({'King': '乾隆'},
                  {'$set': {'King': '乾隆爷'}},
                  upsert=False,  # 如果没有符合条件的数据，默认不插入
                  multi=False)  # 默认值修改第一条匹配的数据

    # 增加新数据
    my_set.update({'name': '范冰冰'},
                  {'$set': {'King': '武则天'}},
                  upsert=True,  # 如果没有待查找的数据，则插入新数据
                  multi=False)  # 默认值修改第一条匹配的数据

    # 给指定数据增加新域，同时修改多条文档
    my_set.update({'King': '康熙'},
                  {'$set': {'King_name': '玄烨'}},
                  multi=True)

    find_data()


def update_many_db():
    # 匹配到多个文档时全部修改，且不需要multi参数
    my_set.update_many({'King': '雍正'},
                       {'$set': {'King_name': '胤禛'}})
    find_data()


def update_one_db():
    # 只修改匹配到的第一条文档
    # 选择不含king_name 字段的数据，添加该字段——只会修改第一个
    my_set.update_one({'King_name': None},
                      {'$set': {'King_name': '弘历'}})
    find_data()

def main():
    # insert_db()
    # remove_db()
    # find_data()
    # find_data_2()
    # find_one()

    # update_db()
    # update_many_db()
    update_one_db()
    pass


if __name__ == '__main__':
    main()
