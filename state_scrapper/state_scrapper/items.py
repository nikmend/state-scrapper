# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class StateScrapperItem(scrapy.Item):
    id_web = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    type = scrapy.Field()
    price = scrapy.Field()
    city = scrapy.Field()
    sector = scrapy.Field()
    address = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    built_area = scrapy.Field()
    private_area = scrapy.Field()
    last_date = scrapy.Field(serializer=str)
    strata = scrapy.Field()
    floors = scrapy.Field()
    antiquity = scrapy.Field()
    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    garages = scrapy.Field()
