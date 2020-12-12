# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
import scrapy, json, re, time
from items import FirstPageInfo, EachPageInfo
from settings import MAX_TO_WRITE_IN_A_FILE

class Crawler1(Spider):
    name = "sslproxiesCrawler"
    page_number = 0
    max_pages_to_crawl = 1
    start_urls = [
        "https://www.sslproxies.org/"
    ]
    xpaths = {
        "ip":
            "//tr[@role='row' and @class]/td[1]/text()",
        "port":
            "//tr[@role='row' and @class]/td[2]/text()",
        "isHttps":
            "//tr[@role='row' and @class]/td[7]/text()"
    }
    new_ip = []
    def parse(self, response):
        ips = response.xpath(self.xpaths["ip"]).extract()
        ports = response.xpath(self.xpaths["port"]).extract()
        isHttps = response.xpath(self.xpaths["isHttps"]).extract()

        for ip, port, isHttp in zip(ips, ports, isHttps):
            if isHttp == "yes":
                # {"ipaddr": "93.152.172.162:23500"},
                self.new_ip.append("{\"ipaddr\":\"https://%s:%s\"},"%(ip, port))
            else:
                self.new_ip.append("{\"ipaddr\":\"http://%s:%s\"},"%(ip, port))

class Crawler2(Spider):
    name = "hide_my_ipCrawler"
    page_number = 0
    max_pages_to_crawl = 1
    start_urls = [
        "https://www.hide-my-ip.com/proxylist.shtml"
    ]
    xpaths = {
        "ip_json":
            "//div[@class='wrapper']/script[3]/text()",
    }
    new_ip = []
    def parse(self, response):
        ips = response.xpath(self.xpaths["ip_json"]).extract_first()
        print(ips)

class Crawler3(Spider):
    name = "data5uCrawler"
    page_number = 0
    max_pages_to_crawl = 1
    start_urls = [
        "http://www.data5u.com/free/gwgn/index.shtml"
    ]
    xpaths = {
        "ip":
            "//ul[@class='l2']/span[1]/li/text()",
        "port":
            "//ul[@class='l2']/span[2]/li/text()",
        "isHttps":
            "//ul[@class='l2']/span[4]/li/text()"
    }
    new_ip = []
    def parse(self, response):
        ips = response.xpath(self.xpaths["ip"]).extract()
        ports = response.xpath(self.xpaths["port"]).extract()
        isHttps = response.xpath(self.xpaths["isHttps"]).extract()

        for ip, port, isHttp in zip(ips, ports, isHttps):
            self.new_ip.append("{\"ipaddr\":\"%s://%s:%s\"},"%(isHttp, ip, port))

class Crawler4(Spider):
    name = "freeproxylistsCrawler"
    page_number = 0
    max_pages_to_crawl = 1
    start_urls = [
        "http://www.freeproxylists.net/"
    ]
    xpaths = {
        "ip":
            "//tr[@class='Odd']/td[1]/a/text()",
        "port":
            "//tr[@class='Odd']/td[2]/text()",
        "isHttps":
            "//tr[@class='Odd']/td[3]/text()"
    }
    new_ip = []
    def parse(self, response):
        ips = response.xpath(self.xpaths["ip"]).extract()
        ports = response.xpath(self.xpaths["port"]).extract()
        isHttps = response.xpath(self.xpaths["isHttps"]).extract()

        for ip, port, isHttp in zip(ips, ports, isHttps):
            self.new_ip.append("{\"ipaddr\":\"%s://%s:%s\"},"%(isHttp, ip, port))