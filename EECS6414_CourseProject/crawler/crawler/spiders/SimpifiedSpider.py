# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
import scrapy, json, re, time, os
from items import FirstPageInfo, EachPageInfo, DownloadItem, DownloadHtml, OverallDownload
from settings import MAX_TO_WRITE_IN_A_FILE, DATA_STORE


def model_name_legalize(string):
    return string.strip().replace("\\", "_").replace("/", "_").replace(":", "_").replace(">", "_") \
        .replace("*", "_").replace("?", "_").replace("\"", "_").replace("<", "_").replace("|", "_")

class FirstPage(Spider):
    name = "SimplifiedSpider"
    page_number = 0
    max_pages_to_crawl = 2
    last_kernel_id = -1
    if os.path.exists(os.path.join(DATA_STORE, "last_id.csv")):
        with open(os.path.join(DATA_STORE, "last_id.csv"), "r") as f:
            last_kernel_id = int(f.readline().split(",")[1])
    #last_kernel_id = 2381851
    start_urls = [
        "https://www.kaggle.com/kernels.json?sortBy=hotness&group=everyone&pageSize={}".format(MAX_TO_WRITE_IN_A_FILE) if last_kernel_id < 0 else
        "https://www.kaggle.com/kernels.json?sortBy=hotness&group=everyone&pageSize={}&after={}".format(MAX_TO_WRITE_IN_A_FILE, last_kernel_id)
    ]
    xpaths = {
        "review":
            "/html/body/pre/text()",
        "info":
            "/html/body/div[2]/div[2]/script[1]/text()",
        "code_url":
            "//li[@class='sc-dsnQBu kmSmsd']/a/@href",
    }
    def parse(self, response):
        _ = response.xpath(self.xpaths["review"]).extract_first()
        if _ is not None: #self.page_number < self.max_pages_to_crawl and ###
            print("####################  page %d ############################" % (self.page_number))
            infos = json.loads(_)
            for i in range(len(infos)):
                id = infos[i]["id"]
                title = model_name_legalize(infos[i]["scriptUrl"])[1:]

                item = FirstPageInfo()
                item["id"] = id
                item["title"] = title
                item["info"] = infos[i]
                yield item
                self.last_kernel_id = id

                page_of_each_kernel = "https://www.kaggle.com" + infos[i]["scriptUrl"]

                item_down = OverallDownload()
                item_down["file_ids"] =  [infos[i]["scriptVersionId"]]
                item_down["title"] = title
                item_down["file_urls"] = [
                    page_of_each_kernel
                ]
                item_down["file_names"] = [
                    "webpages.html",
                ]
                time.sleep(1)
                yield item_down

                item_each_page = EachPageInfo()
                item_each_page["id"] = id
                item_each_page["title"] = title

                if i == len(infos) - 1:
                    last_id = infos[i]["id"]
                    self.page_number += 1
                    time.sleep(1)
                    yield scrapy.Request(
                        "https://www.kaggle.com/kernels.json?sortBy=hotness&group=everyone&pageSize={}&after={}"
                            .format(MAX_TO_WRITE_IN_A_FILE,
                                    last_id),
                         callback=self.parse
                    )
                    # with open("last_id.csv", "a") as f:
                    #     f.write("{},{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    #                            last_id))
        else:
            pass
