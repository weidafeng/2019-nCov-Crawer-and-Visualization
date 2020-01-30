"""
@ProjectName: DXY-2019-nCov-Crawler
@FileName: crawler.py
@Author: Jiabao Lin
@Date: 2020/1/21
"""
from bs4 import BeautifulSoup  # 该模块用于接收一个HTML或XML字符串，然后将其进行格式化，之后遍可以使用他提供的方法进行快速查找指定元素，从而使得在HTML或XML中查找指定元素变得简单。
from service.db import DB  # 菲关系型数据库，以bson格式存储（类似于python的字典，键值对）
from service.countryTypeMap import country_type
import re  # 正则表达式（与bs的属性索引一起，更方便匹配）
import json  # json.load()转换成json格式（ list[dic()] ）
import time
import logging
import datetime
import requests   # 完成浏览器的的各种操作（get，post等）


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}


class Crawler:
    def __init__(self):
        self.session = requests.session()
        self.session.headers.update(headers)
        self.db = DB()
        self.crawl_timestamp = int()

    def run(self):
        while True:
            self.crawler()
            time.sleep(60)

    def crawler(self):
        while True:
            self.crawl_timestamp = int(datetime.datetime.timestamp(datetime.datetime.now()) * 1000)
            try:
                r = self.session.get(url='https://3g.dxy.cn/newh5/view/pneumonia')
            except requests.exceptions.ChunkedEncodingError:
                continue
            soup = BeautifulSoup(r.content, 'lxml')

            overall_information = re.search(r'\{("id".*?)\}', str(soup.find('script', attrs={'id': 'getStatisticsService'})))
            province_information = re.search(r'\[(.*?)\]', str(soup.find('script', attrs={'id': 'getListByCountryTypeService1'})))
            area_information = re.search(r'\[(.*)\]', str(soup.find('script', attrs={'id': 'getAreaStat'})))
            abroad_information = re.search(r'\[(.*)\]', str(soup.find('script', attrs={'id': 'getListByCountryTypeService2'})))
            news = re.search(r'\[(.*?)\]', str(soup.find('script', attrs={'id': 'getTimelineService'})))

            if not overall_information or not province_information or not area_information or not news:
                continue

            self.overall_parser(overall_information=overall_information)
            self.province_parser(province_information=province_information)
            self.area_parser(area_information=area_information)
            self.abroad_parser(abroad_information=abroad_information)
            self.news_parser(news=news)

            break  # 谣言存储在一个json文件里，与上面几种字段不一样

        while True:
            self.crawl_timestamp = int(datetime.datetime.timestamp(datetime.datetime.now()) * 1000)
            try:
                r = self.session.get(url='https://file1.dxycdn.com/2020/0127/797/3393185293879908067-115.json')
            except requests.exceptions.ChunkedEncodingError:
                continue
            # Use try-except to ensure the .json() method will not raise exception.
            try:
                if r.status_code != 200:
                    continue
                elif r.json().get('code') == 'success':
                    self.rumor_parser(rumors=r.json().get('data'))
                    break
                else:
                    continue
            except json.decoder.JSONDecodeError:
                continue

        logger.info('Successfully crawled.')

    def overall_parser(self, overall_information):
        overall_information = json.loads(overall_information.group(0))
        overall_information.pop('id')
        overall_information.pop('createTime')
        overall_information.pop('modifyTime')
        overall_information.pop('imgUrl')
        overall_information.pop('deleted')
        overall_information['countRemark'] = overall_information['countRemark'].replace(' 疑似', '，疑似').replace(' 治愈', '，治愈').replace(' 死亡', '，死亡').replace(' ', '')
        if not self.db.find_one(collection='DXYOverall', data=overall_information):
            overall_information['updateTime'] = self.crawl_timestamp

            self.db.insert(collection='DXYOverall', data=overall_information)

    def province_parser(self, province_information):
        provinces = json.loads(province_information.group(0))
        for province in provinces:
            province.pop('id')
            province.pop('tags')
            province.pop('sort')
            province['comment'] = province['comment'].replace(' ', '')
            if self.db.find_one(collection='DXYProvince', data=province):
                continue
            province['crawlTime'] = self.crawl_timestamp
            province['country'] = country_type.get(province['countryType'])

            self.db.insert(collection='DXYProvince', data=province)

    def area_parser(self, area_information):
        area_information = json.loads(area_information.group(0))
        for area in area_information:
            area['comment'] = area['comment'].replace(' ', '')
            if self.db.find_one(collection='DXYArea', data=area):
                continue
            area['country'] = '中国'
            area['updateTime'] = self.crawl_timestamp

            self.db.insert(collection='DXYArea', data=area)

    def abroad_parser(self, abroad_information):
        countries = json.loads(abroad_information.group(0))
        for country in countries:
            country.pop('id')
            country.pop('tags')
            country.pop('countryType')
            country.pop('provinceId')
            country['country'] = country.get('provinceName')
            country['provinceShortName'] = country.get('provinceName')
            country.pop('cityName')
            country.pop('sort')

            country['comment'] = country['comment'].replace(' ', '')
            if self.db.find_one(collection='DXYAbroad', data=country):
                continue
            country['updateTime'] = self.crawl_timestamp

            self.db.insert(collection='DXYAbroad', data=country)

    def news_parser(self, news):
        news = json.loads(news.group(0))
        for _news in news:
            _news.pop('pubDateStr')
            if self.db.find_one(collection='DXYNews', data=_news):
                continue
            _news['crawlTime'] = self.crawl_timestamp

            self.db.insert(collection='DXYNews', data=_news)

    def rumor_parser(self, rumors):
        for rumor in rumors:
            rumor.pop('score')
            rumor['body'] = rumor['body'].replace(' ', '')
            if self.db.find_one(collection='DXYRumors', data=rumor):
                continue
            rumor['crawlTime'] = self.crawl_timestamp

            self.db.insert(collection='DXYRumors', data=rumor)


if __name__ == '__main__':
    crawler = Crawler()
    crawler.run()
