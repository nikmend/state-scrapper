import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
# -*- coding: utf-8 -*-
import scrapy
import requests
from scrapy.linkextractors import LinkExtractor
from lxml import html
from ..items import StateScrapperItem
from datetime import datetime



class StateSpider(scrapy.Spider):
    name = "stateCommon"
    allowed_domains = ["metrocuadrado.com"]
    start_urls = ('https://www.metrocuadrado.com/venta/bogota/',)
    ajaxurl = 'https://www.metrocuadrado.com/search/list/ajax?mciudad=bogota&currentPage={}&totalPropertiesCount={}&totalUsedPropertiesCount={}&totalNewPropertiesCount={}'
    totalNewPropertiesCount = 0
    totalUsedPropertiesCount = 0
    totalPropertiesCount = 0

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}
        for url in self.start_urls:
            ##yield Request(url, headers=headers)
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response):
        if self.totalPropertiesCount == 0 :
            self.totalNewPropertiesCount= int(response.css('#total-new-properties-count-list::attr(value)').extract()[0])
            self.totalUsedPropertiesCount= int(response.css('#total-used-properties-count-list::attr(value)').extract()[0])
            print("/*"*10)
            print(self.totalNewPropertiesCount, self.totalUsedPropertiesCount)
            self.totalPropertiesCount= self.totalNewPropertiesCount+self.totalUsedPropertiesCount
            print(self.totalPropertiesCount)
            print("/*" * 10)
            for page in range(int(self.totalPropertiesCount / 50)):
                ##yield Request(url, headers=headers)
                self.start_urls.append(self.ajaxurl.format(page, self.totalPropertiesCount, self.totalUsedPropertiesCount,
                                             self.totalNewPropertiesCount))

        for prop in response.css('.detail_wrap'):
            item = StateScrapperItem()
            item['type'] = prop.attrib['propertytype']
            item['id_web'] = prop.attrib['id']
            item['city'] = prop.attrib['cityname']
            item['url'] = prop.css('.content .header .data-details-id::attr(href)').extract()[0]
            item['title'] = prop.css('.content .header .data-details-id>h2::text').extract()[0]
            item['price'] = str(prop.css('.price_desc span[itemprop="price"]::text').extract()[0][1:]).replace('.', '')
            item['built_area'] = prop.css('.price_desc .desc_rs .m2 span:nth_child(2)::text').extract()[0][:-3]
            item['last_date'] = datetime.today().strftime('%Y-%m-%d')
            try:
                item['sector'] = prop.attrib['neighborhood']
            except KeyError as e:
                item['sector'] = 'NULL'
                self.logger.info("Item " + item['id_web'] + " hasn´t sector\n" + "---------" * 6)
            try:
                item['bathrooms'] = prop.css('.price_desc .desc_rs .bathrooms span:nth_child(2)::text').extract()[0]
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

        next_page = response.xpath('.//a[@class="button next"]/@href').extract()
        if next_page:
            next_href = next_page[0]
            next_page_url = 'http://sfbay.craigslist.org' + next_href
            request = scrapy.Request(url=next_page_url)
            yield request
