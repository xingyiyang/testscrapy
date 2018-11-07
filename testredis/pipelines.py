# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi

class TestredisPipeline(object):
    def __init__(self):
        config = {
            "host": settings['MYSQL_HOST'],
            "user": settings['MYSQL_USER'],
            "password": settings['MYSQL_PASS'],
            "database": settings['MYSQL_DB']
        }
        # 指定数据库模块名和数据库参数
        self.dbpool = adbapi.ConnectionPool("pymysql", **config)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 处理异常
        query.addErrback(self.handle_error, item, spider)

    # 处理异步插入的异常
    def handle_error(self, failure, item, spider):
        print(failure)

    def do_insert(self, cursor, item):
        try:
            sql = "INSERT INTO tencentjob(jobname,jobtype,people,adrs,fabu) VALUES(%s,%s,%s,%s,%s)"
            values = (item['zwmc'], item['zwlb'], item['rs'], item['dd'], item['fbsj'])
            cursor.execute(sql, values)
            return item
        except Exception as err:
            pass