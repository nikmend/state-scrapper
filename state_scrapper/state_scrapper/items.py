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
    type_ads = scrapy.Field()
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
    ## params
    description = scrapy.Field()
    postal_code = scrapy.Field()
    features = scrapy.Field()  # esto es un Json
    agency_name = scrapy.Field()
    agency_address = scrapy.Field()
    agency_contact = scrapy.Field()
    agency_phone = scrapy.Field()
