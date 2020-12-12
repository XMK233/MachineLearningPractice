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
    name = "AuthorAndDatasetSpider"
    page_number = 0
    max_pages_to_crawl = 2
    last_kernel_id = -1
    if os.path.exists(os.path.join(DATA_STORE, "last_id.csv")):
        with open(os.path.join(DATA_STORE, "last_id.csv"), "r") as f:
            last_kernel_id = int(f.readline().split(",")[1])
    start_urls = [
        "https://www.kaggle.com"
    ]

    def parse(self, response):
        file_path = "J:\\EECS_6414\\Data\\19-02-03\\KernelInfo_{}.json"
        json_paths = get_project_settings().get('START_NUMBERS')
        data_store = get_project_settings().get("DATA_STORE")
        for json_path in json_paths:
            if not os.path.exists(file_path.format(json_path)):
                continue
            with open(os.path.join(data_store, "AuthorDataset_StartFromFile.csv"), "a") as ff:
                ff.write("{},{}\n".format(time.ctime(), json_path))
            with open(file_path.format(json_path), "r") as j:
                print(file_path.format(json_path))
                kernels = json.load(j)
            authorUrls = []
            datasetUrls = []
            for kernel in kernels:
                info = kernel["info"]
                title = kernel["title"]

                #item = OverallDownload()
                authorUrls.append(info["author"]["profileUrl"])
                datasetUrls.extend([ds["dataSourceUrl"] for ds in info["dataSources"] if ds is not None])
            # for author in authorUrls:
            authorUrls = list(set(authorUrls))
            print("author urls. this number is approximate: ", len(authorUrls))
            datasetUrls = list(set(datasetUrls))
            print("dataset urls. this number is approximate: ", len(datasetUrls))
            ######
            item_author = DownloadHtml()
            item_author["title"] = "author_pages"
            item_author["file_name"] = [au[1:] + ".html" for au in authorUrls]
            item_author["file_url"] = [self.start_urls[0] + au for au in authorUrls]
            # print(item_author)
            yield item_author

            item_dataset = DownloadHtml()
            item_dataset["title"] = "dataset_pages"
            item_dataset["file_name"] = [dsu[1:].replace("/", "_") + ".html" for dsu in datasetUrls if dsu is not None]#
            item_dataset["file_url"] = [self.start_urls[0] + dsu for dsu in datasetUrls if dsu is not None]#
            # print(item_dataset)
            yield item_dataset
