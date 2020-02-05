# 学习pymongo

## 增删改查

``` bash
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


#############################
```

## 部分操作符
```
## 符号含义示例
$lt小于{'age': {'$lt': 20}}
$gt大于{'age': {'$gt': 20}}
$lte小于等于{'age': {'$lte': 20}}
$gte大于等于{'age': {'$gte': 20}}
$ne不等于{'age': {'$ne': 20}}
$in在范围内{'age': {'$in': [20, 23]}}
$nin不在范围内{'age': {'$nin': [20, 23]}}
$exists存在某个字段{'gender': {'$exists': True}  # 找出所有存在gender字段的数据

## 其他符号含义示例示例含义
$regex匹配正则{'name': {'$regex': '^M.*'}}name以M开头
$exists属性是否存在{'name': {'$exists': True}}name属性存在
$type类型判断{'age': {'$type': 'int'}}age的类型为int
$mod数字模操作{'age': {'$mod': [5, 0]}}年龄模5余0
$text文本查询{'$text': {'$search': 'Mike'}}text类型的属性中包含Mike字符串
$where高级条件查询{'$where': 'obj.fans_count == obj.follows_count'}自身粉丝数等于关注数

```
这些操作的更详细用法在可以在MongoDB官方文档找到：  

https://docs.mongodb.com/manual/reference/operator/query/


## 索引和聚合操作
```bash
# MongoDB命令行操作

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
```

## 在MongoDB数据库存储文件
```bash

# 在MongoDB存储文件
比如我想把桌面上的wake.MP3文件放到wdf_files数据库里（没有则自动新建该数据库）

# shell 命令
C:\Users\wdf>cd Desktop  # 进入存放文件的路径（桌面）

C:\Users\wdf\Desktop>mongofiles -d wdf_files put Wake.mp3   # put函数
2020-02-05T12:00:00.490+0800    connected to: mongodb://localhost/
2020-02-05T12:00:00.645+0800    added gridFile: Wake.mp3


# 打开mongo，查看数据库
> show dbs
2019-nCov  0.001GB
admin      0.000GB
config     0.000GB
local      0.000GB
wdf        0.000GB
wdf_files  0.011GB   # 刚才新建的数据库，里面存放了mp3文件
> use wdf_files      # 指定该数据库
switched to db wdf_files
> show tables        # 查看该数据库里的内容
fs.chunks            # 默认有两个，一个分块存放数据（分块的好处是不需要连续的空间）
fs.files             # 另一个只存放索引（链接各个分块）
> db.fs.files.find()
{ "_id" : ObjectId("5e3a3dc03c40c5c327b6a129"), "length" : NumberLong(11346754), "chunkSize" : 261120, "uploadDate" : ISODate("2020-02-05T04:00:00.644Z"), "filename" : "Wake.mp3", "metadata" : {  } }
> db.fs.chunks.find()    # 不建议查看——真实存放文件，通过ObjectId与files相连


## MongoDB GridFS
GridFS 用于存储和恢复那些超过16M（BSON文件限制）的文件(如：图片、音频、视频等)。
GridFS 也是文件存储的一种方式，但是它是存储在MonoDB的集合中。
GridFS 可以更好的存储大于16M的文件。
GridFS 会将大文件对象分割成多个小的chunk(文件片段),一般为256k/个,每个chunk将作为MongoDB的一个文档(document)被存储在chunks集合中。
GridFS 用两个集合来存储一个文件：fs.files与fs.chunks。
每个文件的实际内容被存在chunks(二进制数据)中,和文件有关的meta数据(filename,content_type,还有用户自定义的属性)将会被存在files集合中。
以下是简单的 fs.files 集合文档：

{
   "filename": "test.txt",
   "chunkSize": NumberInt(261120),
   "uploadDate": ISODate("2014-04-13T11:32:33.557Z"),
   "md5": "7b762939321e146569b07f72c62cca4f",
   "length": NumberInt(646)
}
以下是简单的 fs.chunks 集合文档：

{
   "files_id": ObjectId("534a75d19f54bfec8a2fe44b"),
   "n": NumberInt(0),
   "data": "Mongo Binary Data"
}


## GridFS 添加文件
使用 GridFS 的 put 命令来存储 mp3 文件。 调用 MongoDB 安装目录下bin的 mongofiles.exe工具。

打开命令提示符，进入到MongoDB的安装目录的bin目录中，找到mongofiles.exe，并输入下面的代码：
>mongofiles.exe -d gridfs put song.mp3
    -d gridfs 指定存储文件的数据库名称，如果不存在该数据库，MongoDB会自动创建。
    Song.mp3 是音频文件名。

使用以下命令来查看数据库中文件的文档：
>db.fs.files.find()
以上命令执行后返回以下文档数据：

{
   _id: ObjectId('534a811bf8b4aa4d33fdf94d'), 
   filename: "song.mp3", 
   chunkSize: 261120, 
   uploadDate: new Date(1397391643474), md5: "e4f53379c909f7bed2e9d631e15c1c41",
   length: 10401959 
}
我们可以看到 fs.chunks 集合中所有的区块，以下我们得到了文件的 _id 值，我们可以根据这个 _id 获取区块(chunk)的数据：

>db.fs.chunks.find({files_id:ObjectId('534a811bf8b4aa4d33fdf94d')})
以上实例中，查询返回了 40 个文档的数据，意味着mp3文件被存储在40个区块中。
```

