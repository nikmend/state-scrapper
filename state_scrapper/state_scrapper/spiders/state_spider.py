import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
# -*- coding: utf-8 -*-
import scrapy
from ..items import StateScrapperItem

from datetime import datetime


class StateSpider(scrapy.Spider):
    name = "stateCommon"
    allowed_domains = ["metrocuadrado.com"]
    start_urls = ['https://www.metrocuadrado.com/venta/bogota/', ]
    ajaxurl = 'https://www.metrocuadrado.com/search/list/ajax?mciudad=bogota&currentPage={}&totalPropertiesCount={}&totalUsedPropertiesCount={}&totalNewPropertiesCount={}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}
    totalNewPropertiesCount = 0
    totalUsedPropertiesCount = 0
    totalPropertiesCount = 0

    def populate_Starts(self):

        print("/*" * 10)
        print(self.totalNewPropertiesCount, self.totalUsedPropertiesCount)
        self.totalPropertiesCount = self.totalNewPropertiesCount + self.totalUsedPropertiesCount
        print(self.totalPropertiesCount)
        print("/*" * 10)
        for page in range(1, int(self.totalPropertiesCount / 50) + 1):
            self.start_urls.append(self.ajaxurl.format(page, self.totalPropertiesCount, self.totalUsedPropertiesCount,
                                                       self.totalNewPropertiesCount))
        print('added ' + str(len(self.start_urls)) + ' new Urls')

    def start_requests(self):
        for url in self.start_urls:
            print('????? IN LOOP: ', url)
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        if self.totalPropertiesCount == 0:
            self.totalNewPropertiesCount = int(
                response.css('#total-new-properties-count-list::attr(value)').extract()[0])
            self.totalUsedPropertiesCount = int(
                response.css('#total-used-properties-count-list::attr(value)').extract()[0])
            self.populate_Starts()
            for url in self.start_urls[10:30]:
                print('????? IN NESTED LOOP: ', url)
                yield scrapy.Request(url=url, method='POST', callback=self.parse, headers=self.headers)

        else:
            print('Im out bitch')
            for prop in response.css('.detail_wrap'):
                if prop.attrib['businesstype'] in ["Venta y Arriendo", 'venta']:
                    item = StateScrapperItem()
                    item['type'] = prop.attrib['propertytype'] + " - " + prop.attrib['businesstype']
                    item['id_web'] = prop.attrib['id']
                    item['city'] = prop.attrib['cityname']
                    item['url'] = prop.css('.content .header .data-details-id::attr(href)').extract()[0]
                    item['title'] = prop.css('.content .header .data-details-id>h2::text').extract()[0]
                    item['price'] = str(prop.css('.price_desc span[itemprop="price"]::text').extract()[0][1:]).replace(
                        '.', '')
                    item['built_area'] = prop.css('.price_desc .desc_rs .m2 span:nth_child(2)::text').extract()[0][:-3]
                    item['last_date'] = datetime.today().strftime('%Y-%m-%d')
                    try:
                        item['sector'] = prop.attrib['neighborhood']
                    except KeyError as e:
                        item['sector'] = 'NULL'
                        self.logger.info("Item " + item['id_web'] + " hasn´t sector\n" + "---------" * 6)
                    try:
                        item['bathrooms'] = \
                            prop.css('.price_desc .desc_rs .bathrooms span:nth_child(2)::text').extract()[0]
                    except IndexError as e:
                        item['bathrooms'] = 'NULL'
                        self.logger.info("Item " + item['id_web'] + " hasn´t bathrooms\n" + "---------" * 6)
                    try:
                        item['bedrooms'] = prop.css('.price_desc .desc_rs .rooms span:nth_child(2)::text').extract()[0]
                    except IndexError as e:
                        item['bedrooms'] = 'NULL'
                        self.logger.info("Item " + item['id_web'] + " hasn´t bedrooms\n" + "---------" * 6)
                    try:
                        item['garages'] = prop.css('.price_desc .desc_rs .garages span::text').extract()[0]
                    except IndexError as e:
                        item['garages'] = 'NULL'
                        self.logger.info("Item " + item['id_web'] + " hasn´t garages\n" + "---------" * 6)

                    yield item
