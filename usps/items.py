# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UspsCollectionBoxItem(scrapy.Item):
    name = scrapy.Field()
    address = scrapy.Field()
    collection_times = scrapy.Field()
    location_id = scrapy.Field()
    lat = scrapy.Field()
    lon = scrapy.Field()
