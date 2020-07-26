# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import NotConfigured
import mysql.connector
import json


class StateScrapperPipeline(object):

    def open_spider(self, spider):
        self.file = open('items.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        # print(item)
        # self.file.write(line)
        return item


class DatabasePipeline(object):

    def __init__(self, database, user, password, host):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.items = []
        self.query = ""

    def connectDB(self):
        self.conn = mysql.connector.connect(
            database=self.database,
            host=self.host,
            user=self.user, password=self.password,
            charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        return item

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict("DB_SETTINGS")
        if not db_settings:  # if we don't define db config in settings
            raise NotConfigured  # then reaise error
        database = db_settings['database']
        user = db_settings['user']
        password = db_settings['password']
        host = db_settings['host']
        return cls(database, user, password, host)  # returning pipeline instance

    def open_spider(self, spider):
        self.connectDB()

    def process_item(self, item, spider):

        placeholders = ', '.join(['%s'] * len(item))
        columns = ', '.join(item.keys())
        self.query = "INSERT INTO %s ( %s ) VALUES ( %s )" % ("states", columns, placeholders)
        self.items.extend([item.values()])

        return item

    def close_spider(self, spider):
        try:
            self.cursor.executemany(self.query, self.items)
            self.conn.commit()
            print("MYSQL   " + str(self.cursor.rowcount)+  "record inserted.")
            self.items = []
        except Exception as e:
            if 'MySQL server has gone away' in str(e):
                self.connectDB()
                spider.cursor.executemany(self.query, self.items)
                self.items = []
            else:
                raise e
        self.conn.close()
