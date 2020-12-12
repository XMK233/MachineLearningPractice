# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
import scrapy, json, re, time, os,tqdm
from items import FirstPageInfo, EachPageInfo, DownloadItem, DownloadHtml, OverallDownload
from settings import MAX_TO_WRITE_IN_A_FILE, DATA_STORE
from scrapy.utils.project import get_project_settings

def model_name_legalize(string):
    return string.strip().replace("\\", "_").replace("/", "_").replace(":", "_").replace(">", "_") \
        .replace("*", "_").replace("?", "_").replace("\"", "_").replace("<", "_").replace("|", "_")

class FirstPage(Spider):
    name = "SplitPageSpider"
    page_number = 0
    max_pages_to_crawl = 2
    last_kernel_id = -1

    start_urls = [
        "https://www.kaggle.com/"
    ]

    def parse(self, response):
        split_file = get_project_settings().get("SPLIT_FILE")
        json_paths = get_project_settings().get('START_NUMBERS')

        split_dir = get_project_settings().get("SPLIT_DIR")
        file_store = get_project_settings().get("FILES_STORE")

        for json_path in json_paths:

            if not os.path.exists(split_file.format(json_path)):
                continue

            with open(os.path.join(file_store, "AuthorDataset_StartFromFile.csv"), "a") as ff:
                ff.write("{},{}\n".format(time.ctime(), json_path))

            with open(split_file.format(json_path), "r") as f:
                urls = f.readlines()
                ##VERSION 1: item for each url
                for url in tqdm.tqdm(urls):
                    url = url.strip()
                    item_author = DownloadHtml()
                    item_author["title"] = "{}".format(json_path)
                    item_author["file_name"] = [url.replace("/", "_")[1:] + ".html"]
                    item_author["file_url"] = [self.start_urls[0] + url]

                    yield item_author

                # names = []
                # urls_modified = []
                # for url in urls:
                #     url = url.strip()
                #     names.append(url.replace("/", "_")[1:] + ".html")
                #     urls_modified.append(self.start_urls[0] + url)
                # item = DownloadHtml()
                # item["title"] = "{}".format(json_path)
                # item["file_name"] = names
                # item["file_url"] = urls_modified
                # yield item

