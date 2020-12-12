# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class FirstPageInfo(scrapy.Item):
    title = scrapy.Field()
    id = scrapy.Field()
    info = scrapy.Field()
    pass

class EachPageInfo(scrapy.Item):
    title = scrapy.Field()
    id = scrapy.Field()
    info = scrapy.Field()
    pass

class DownloadItem(scrapy.Item):
    title = scrapy.Field()
    #file_name = scrapy.Field()
    file_url =scrapy.Field()
    files = scrapy.Field()
    pass

class DownloadHtml(scrapy.Item):
    title = scrapy.Field()
    file_name = scrapy.Field()
    file_url = scrapy.Field()
    files = scrapy.Field()
    pass

class OverallDownload(scrapy.Item):
    title = scrapy.Field()
    file_ids = scrapy.Field()
    file_names = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    pass

class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
