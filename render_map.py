#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:           wdf
# datetime:         1/30/2020 8:28 PM
# software:         PyCharm
# project name:     DXY-2019-nCoV-Crawler 
# file name:        render_map
# description:      根据爬取的各省确诊人数，借助第三方库实现地图形式的可视化
# usage:            

from service import fetch_data
from pyecharts import Map
import numpy as np

provinceShortName, confirmedCount = fetch_data.get_data_from_db()

# value = np.array(confirmedCount)
# value = np.log10(value)  # 可以理解为归一化，因为湖北人数是其余各省的10-100倍，很不均衡，导致颜色分布集中于很小的区间

map = Map("2019-nCov 各省确诊数据统计", width=1000, height=800)
map.add("", attr=provinceShortName, value=confirmedCount, is_map_symbol_show=True, maptype="china", is_visualmap=True,
        visual_text_color='#000', is_label_show=True, visual_range=[np.min(confirmedCount)*10, np.max(confirmedCount)//10])

map.render('results.html')
