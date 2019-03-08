# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class RgspoiderPipeline(ImagesPipeline):

    def get_media_requests(self, items, info):
        print(items)
        title = items['title']
        word = items['word']
        for image_url in items['image_urls']:
            yield scrapy.Request(image_url, meta={'title': title, 'word': word})

    def file_path(self, request, response=None, info=None):
        filename = r'full\%s\%s\%s' % (request.meta['title'], request.meta['word'], request.url[-6:])
        return filename