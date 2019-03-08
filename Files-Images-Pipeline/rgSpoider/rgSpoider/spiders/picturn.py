# -*- coding: utf-8 -*-
import scrapy
from ..items import RgspoiderItem


class PicturnSpider(scrapy.Spider):

    name = 'picturn'
    allowed_domains = ['xxxxxx.com']
    start_urls = ['http://xxxxxx/index.html']

    def parse(self, response):
        select = response.xpath('//*[@id="body"]/div[2]/ul//li')
        for i in select:
            URL = i.xpath('a/@href').extract()[0]
            title = i.xpath('a/text()').extract()[0]
            yield scrapy.Request(
                response.urljoin(URL), callback=self.parse_ml, meta={'title': title})

    def parse_ml(self, response):
        mulu = response.xpath('//li[@class="zxsyt"]/a')
        title = response.meta['title']
        for i in mulu:
            urls = i.xpath('@href').extract()[0]
            word = i.xpath('text()').extract()[0]
            yield scrapy.Request(
                response.urljoin(urls), callback=self.parse_pict,
                meta={'word': word, 'title': title})

        next_url = response.xpath('//font[@class="PageCss"]/..//a/@href').extract()
        for nuel in next_url:
            title = response.meta['title']
            yield scrapy.Request(response.urljoin(nuel), callback=self.parse_ml,
                                 meta={'title': title})

    def parse_pict(self, response):
        items = RgspoiderItem()
        items['title'] = response.meta['title']
        items['word'] = response.meta['word']
        pict = response.xpath('//div[@class="temp23"]//a/@href').extract()
        items['image_urls'] = pict
        yield items


