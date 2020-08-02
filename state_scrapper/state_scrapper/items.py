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
    address = scrapy.Field() #TODO: lookup in https://reverse.geocoder.ls.hereapi.com/6.2/reversegeocode.json?apiKey=w0AqGhEuRk7POniPcharjnQ7uKIWgvFhJZbbaAe2hOw&mode=retrieveAddresses&prox=4.724455,-74.03006
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
    features = scrapy.Field() #esto es un Json
    agency_name = scrapy.Field()
    agency_address = scrapy.Field()
    agency_contact = scrapy.Field()
    agency_phone = scrapy.Field()



