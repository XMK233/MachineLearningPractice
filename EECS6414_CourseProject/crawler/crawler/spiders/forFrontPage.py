# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
import scrapy, json, re, time
from items import FirstPageInfo, EachPageInfo
from settings import MAX_TO_WRITE_IN_A_FILE

class FirstPage(Spider):
    name = "FrontPageSpider"
    page_number = 0
    max_pages_to_crawl = 1
    start_urls = [
        "https://www.kaggle.com/kernels.json?sortBy=hotness&group=everyone&pageSize=%d" %(MAX_TO_WRITE_IN_A_FILE)
    ]
    xpaths = {
        "review":
            "/html/body/pre/text()",
        "info":
            "/html/body/div[2]/div[2]/script[1]/text()",
    }
    def parse(self, response):
        _ = response.xpath(self.xpaths["review"]).extract_first()
        if self.page_number < self.max_pages_to_crawl and _ is not None: #
            print("####################  page %d ############################" % (self.page_number))
            infos = json.loads(_)
            for i in range(len(infos)):
                item = FirstPageInfo()
                item["info"] = infos[i]
                yield item

                page_of_each_kernel = "https://www.kaggle.com" + infos[i]["scriptUrl"]
                item_each_page = EachPageInfo()
                item_each_page["id"] = infos[i]["id"]
                item_each_page["title"] = infos[i]["title"]
                # each page item
                #time.sleep(10)
                yield scrapy.Request(
                        page_of_each_kernel,
                        meta={"item": item_each_page},
                         callback=self.parse_each_page
                    )
                # next page
                if i == len(infos) - 1:
                    last_id = infos[i]["id"]
                    self.page_number += 1
                    #time.sleep(10)
                    yield scrapy.Request(
                        self.start_urls[0] + "&after=%d" %last_id,
                         callback=self.parse
                    )
        else:
            pass

    def parse_each_page(self, response):
        item_each_page = response.meta["item"]

        _ = response.xpath(self.xpaths["info"]).extract_first()
        p = re.compile("Kaggle\.State\.push\(\{[\s\S]*\}\)\;")
        info = p.findall(_)[0].replace("Kaggle.State.push(", "")[0:-2]
        item_each_page["info"] = json.loads(info)
        yield item_each_page

