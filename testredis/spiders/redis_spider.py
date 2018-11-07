# -*- coding: utf-8 -*-
import scrapy
from testredis.items import TestredisItem


class RedisSpiderSpide(scrapy.Spider):
    name = 'redis_spider'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php']

    def parse(self, response):
        # 循环电影条目
        zhaoping_list = response.xpath("//table[@class='tablelist']//tr")[1:11]
        for i_item in zhaoping_list:
            zhaoping_item = TestredisItem()
            # 职位名称
            zhaoping_item['zwmc'] = i_item.xpath(".//td[1]//text()").extract_first()
            # 职位类别
            zhaoping_item['zwlb'] = i_item.xpath(".//td[2]//text()").extract_first()
            # 人数
            zhaoping_item['rs'] = i_item.xpath(".//td[3]//text()").extract_first()
            # 地点
            zhaoping_item['dd'] = i_item.xpath(".//td[4]//text()").extract_first()
            # 发布时间
            zhaoping_item['fbsj'] = i_item.xpath(".//td[5]//text()").extract_first()
            print(zhaoping_item)
            # 将数据yield到pipeline里面，进行数据的清洗和存储
            yield zhaoping_item
        # 解析下一页
        next_link = response.xpath("//div[@class='pagenav']//a[@id='next']//@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://hr.tencent.com/" + next_link, callback=self.parse)
