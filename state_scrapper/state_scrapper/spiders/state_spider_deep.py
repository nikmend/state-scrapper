import json

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
# -*- coding: utf-8 -*-
import scrapy
from ..items import StateScrapperItem
from ..utilsMobicrol import reverseAddress, cleanContact
from unidecode import unidecode
from datetime import datetime


class StateSpiderDeep(scrapy.Spider):
    name = "stateCommonDeep"
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

    def populateProy(self, response):
        # Es un proyecto
        item = StateScrapperItem()
        property_info = self.getInfo(response)
        item['id_web'] = response.css('#namepropertyId::attr(value)').extract_first()
        item['title'] = response.css('title::text').extract_first().strip(' \t\n\r')
        item['description'] = response.css('#pDescription::text').extract_first()
        item['url'] = response.css('#requestURI::attr(value)').extract_first()
        item['type_ads'] = response.css('#propertyType::attr(value)').extract_first()
        item['price'] = str(response.css('#propertyPriceCalculo::attr(value)').extract_first()).replace('.', '')
        item['agency_name'] = response.css('.datos_inmobiliaria p:nth_child(1)::text').extract()[0]
        item['city'] = response.css('#cityname::attr(value)').extract_first()
        item['sector'] = response.css('#nomBarrio::attr(value)').extract_first()
        item['latitude'] = response.css('#latitude::attr(value)').extract_first()
        item['longitude'] = response.css('#longitude::attr(value)').extract_first()
        if  len(item['longitude'])>1:
            myAdd = reverseAddress(item['latitude'], item['longitude'])
            item['address'] = myAdd['Street'] + '-' + myAdd.get('HouseNumber', '0')
        else:
            item['address'] = None
        item['postal_code'] = myAdd['PostalCode']
        item['built_area'] = response.css('#areaConstruida::attr(value)').extract_first()
        item['private_area'] = response.css('#areaPrivada::attr(value)').extract_first()
        item['last_date'] = datetime.today().strftime('%Y-%m-%d')
        item['strata'] = property_info.get('ESTRATO', None)
        item['floors'] = property_info.get('NÚMERO_DE_NIVELES',None)
        item['antiquity'] = property_info['TIEMPO_DE_CONSTRUIDO']
        item['bedrooms'] = response.css('#numBanos::attr(value)').extract_first()
        item['bathrooms'] = response.css('#numBanos::attr(value)').extract_first()
        item['garages'] = response.css('#numGaraje::attr(value)').extract_first()
        item['features'] = json.dumps(property_info)
        item['agency_address'] = response.css('.datos_inmobiliaria p:nth_child(2)::text').extract()[0]
        item['agency_contact'] = cleanContact( response.css('.detalle_mensaje_contacto ul li::text').extract())
        try:
            item['agency_phone'] = \
                response.css('.link-whatsapp-contact::attr(onclick)').extract_first()[27:].split('?')[0]
        except :
            item['agency_phone'] = None
            self.logger.info("Item " + str(item['title']) + " hasn´t agency_phone\n" + "---------" * 6)
        return item

    def populateProp(self, response):
        item = StateScrapperItem()
        property_info = self.getInfo(response)
        item['id_web'] = response.css('#propertyId::attr(value)').extract_first()
        item['title'] = response.css('title::text').extract_first().strip(' \t\n\r')
        item['description'] = response.css('#pDescription::text').extract_first()
        item['url'] = response.css('#requestURI::attr(value)').extract_first()
        item['type_ads'] = response.css('#propertyType::attr(value)').extract_first()
        item['price'] = response.css('#propertyPrice::attr(value)').extract_first().replace('.', '')
        item['agency_name'] = response.css('#nombreEmpresa::attr(value)').extract()[0]
        item['city'] = response.css('#cityname::attr(value)').extract_first()
        item['sector'] = response.css('#nomBarrio::attr(value)').extract_first()
        item['latitude'] = response.css('#latitude::attr(value)').extract_first()
        item['longitude'] = response.css('#longitude::attr(value)').extract_first()
        if len(item['longitude']) > 1:
            myAdd = reverseAddress(item['latitude'], item['longitude'])
            item['address'] = myAdd['Street'] + '-' + myAdd.get('HouseNumber', '0')
        else:
            item['address'] = None
        item['postal_code'] = myAdd['PostalCode']
        item['built_area'] = response.css('#areaConstruida::attr(value)').extract_first()
        item['private_area'] = response.css('#areaPrivada::attr(value)').extract_first()
        item['last_date'] = datetime.today().strftime('%Y-%m-%d')
        item['strata'] = property_info.get('ESTRATO', None)
        item['floors'] = property_info.get('NUMERO_DE_NIVELES',None)
        item['antiquity'] = property_info.get('TIEMPO_DE_CONSTRUIDO',None)
        item['bedrooms'] = response.css('#numBanos::attr(value)').extract_first()
        item['bathrooms'] = response.css('#numBanos::attr(value)').extract_first()
        item['garages'] = response.css('#numGaraje::attr(value)').extract_first()
        item['features'] = json.dumps(property_info)

        try:
            item['agency_address'] = response.css('.datos_inmobiliaria p:nth_child(2)::text').extract()[0]
        except:
            item['agency_address'] = None
        item['agency_contact'] = cleanContact( response.css('.detalle_mensaje_contacto ul li::text').extract())
        try:
            item['agency_phone'] = \
                response.css('.link-whatsapp-contact::attr(onclick)').extract_first()[27:].split('?')[0]
        except:
            item['agency_phone'] = None
            self.logger.info("Item " + str(item['title']) + " hasn´t agency_phone\n" + "---------" * 6)
        return item

    def start_requests(self):
        for url in self.start_urls:
            print('????? IN LOOP: ', url)
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        if self.totalPropertiesCount == 0:
            self.totalNewPropertiesCount = int(
                response.css('#total-new-properties-count-list::attr(value)').extract_first())
            self.totalUsedPropertiesCount = int(
                response.css('#total-used-properties-count-list::attr(value)').extract_first())
            self.populate_Starts()
            for url in self.start_urls[10:12]:
                print('????? IN NESTED LOOP: ', url)
                for prop in response.css('.detail_wrap'):
                    print('????? IN SUB NESTED LOOP: ',
                          prop.css('.content .header .data-details-id::attr(href)').extract_first())
                    if '/arriendo' not in prop.css('.content .header .data-details-id::attr(href)').extract_first():
                        yield scrapy.Request(url=prop.css('.content .header .data-details-id::attr(href)').extract_first(),
                                             method='GET', callback=self.parse, headers=self.headers)
        else:
            propertyTypeIdHidden = response.css('#propertyTypeIdHidden::attr(value)').extract()
            if len(propertyTypeIdHidden) > 0:
                print('Es un proyecto')
                item = self.populateProy(response)
            else:
                print('es Venta y arriendo')
                item = self.populateProp(response)
            yield item

    def getInfo(self, response):
        info_Dict= {}
        for dl in response.css('.m_property_info_details dl'):
            info_Dict[unidecode(dl.css('h3::text').extract_first().upper().strip()).replace(' ', '_')] = unidecode(dl.css('h4::text').extract_first().strip())
        for dl in response.css('.m_m_collapsable_wrapper_content  dl'):
            info_Dict[unidecode(dl.css('h3::text').extract_first().upper().strip()).replace(' ', '_')] = unidecode(dl.css('h4::text').extract_first().strip())
        complementsAndFinishes = []
        for h4 in response.css('.m_property_info_details.services.complements h4'):
            complementsAndFinishes.append(unidecode(h4.css('::text').extract()[0].strip()))
        info_Dict['complementsAndFinishes'] = complementsAndFinishes
        return info_Dict


