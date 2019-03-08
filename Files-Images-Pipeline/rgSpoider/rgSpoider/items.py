# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RgspoiderItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    title = scrapy.Field()
    word = scrapy.Field()
    url = scrapy.Field()
