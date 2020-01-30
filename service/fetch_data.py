#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:           wdf
# datetime:         1/30/2020 8:14 PM
# software:         PyCharm
# project name:     DXY-2019-nCoV-Crawler 
# file name:        fetch_data
# description:      从本地MongoDB数据库提取出各省的确诊人数
# usage:            

import pandas as pd
import pymongo
from service.db import client, db

def get_data_from_db(client=client, db=db, to_csv=False):
    '''
    :param to_csv: 是否输出csv文件
    :return:
    '''
    # 数据表
    WUHAN_DB = db["DXYProvince"]

    # 将mongodb中的数据读出
    data = pd.DataFrame(list(WUHAN_DB.find({}, {'_id': 0, 'comment': 0, 'country': 0, 'countryType': 0, 'modifyTime': 0,
                                                'operator': 0, 'provinceName': 0, 'provinceId': 0, 'crawlTime': 0,
                                                'createTime': 0, 'cityName': 0, 'suspectedCount': 0}).sort('confirmedCount',
                                                                                                           pymongo.DESCENDING)))
    # 查看数据大小(行列)
    # print(data.shape)  # (34, 16) 34个省，16维数据
    # 查看数据行索引（head）
    # print(data.columns)
    # 查看前几行数据
    # print(data.head(3))

    provinceShortName = data['provinceShortName'].tolist()
    confirmedCount = data['confirmedCount'].tolist()

    print(dict(zip(provinceShortName, confirmedCount)))

    if to_csv:
        # 保存为csv格式
        data.to_csv('2019nCov.csv', encoding='utf-8', index=False)
        # 读取csv数据
        # df = pd.read_csv('wuhan.csv', low_memory=False, index_col=0)
    return provinceShortName, confirmedCount


if __name__ == '__main__':
    get_data_from_db(to_csv=False)
