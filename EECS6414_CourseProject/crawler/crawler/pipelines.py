# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonItemExporter
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline
import os, json, re, scrapy, shutil, time
from scrapy.utils.project import get_project_settings
from settings import MAX_TO_WRITE_IN_A_FILE, DATA_STORE
from items import FirstPageInfo, EachPageInfo, DownloadItem, DownloadHtml, OverallDownload
import wget

data_directory = DATA_STORE

def json_reformed(js):
    # return a json in different format: {modelname: {model information}, modelname1: {model information}, .....}
    new_list = []
    for j in js:
        new_dic = {}
        tmp = j.pop("info")
        id = tmp.pop("id")
        new_dic[id] = tmp
        new_list.append(new_dic)
    return new_list

class DoSomethingBeforeExit(object):
    def close_spider(self, spider):
        with open("{}/last_id.csv".format(DATA_STORE), "w") as f:
            f.write("{},{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                   spider.last_kernel_id))

class SaveIPAddress(object):
    def close_spider(self, spider):
        with open("{}/new_ip.txt".format(DATA_STORE), "a") as f:
            for i in spider.new_ip:
                f.write("{}\n".format(i))
            f.write("\n".format(i))

class OverallDownloadPipeline(FilesPipeline):
    file_store = get_project_settings().get('FILES_STORE')
    def get_media_requests(self, item, info):
        if isinstance(item, OverallDownload):
            print("in overall pipeline: ", type(item), item)
            for url in item["file_urls"]:
                time.sleep(1)
                yield scrapy.Request(url)
        else:
            return
    def item_completed(self, results, item, info):
        if isinstance(item, OverallDownload):
            print("in overall pipeline: ", type(item), item)

            img_path = os.path.join(self.file_store, item["title"])
            if os.path.exists(img_path) == False:
                os.makedirs(img_path)
            for i in range(len(results)):
                ok, x = results[i]
                if not ok:
                    continue
                else:
                    path = x["path"]
                    code_name = wget.download("https://www.kaggle.com/kernels/scriptcontent/{}/download".format(item['file_ids'][i]))
                    shutil.move(code_name, os.path.join(img_path, code_name))
                    shutil.move(self.file_store + "\\" + path, img_path + "\\" + item['file_names'][i])

            # image_paths = [x['path'] for ok, x in results if ok]
            # img_path = os.path.join(self.file_store, item["title"])
            # if os.path.exists(img_path) == False:
            #     os.makedirs(img_path)
            # for i in range(len(image_paths)):
            #     code_name = wget.download("https://www.kaggle.com/kernels/scriptcontent/{}/download".format(item['file_ids'][i]))
            #     shutil.move(code_name, os.path.join(img_path, code_name))
            #     shutil.move(self.file_store + "\\" + image_paths[i], img_path + "\\" + item['file_names'][i])
            #     print("%s move successfully\n\n" %(img_path + "\\" + item['file_names'][i]))
            return item
        return

# class MyfilesPipeline(FilesPipeline):
#     file_store = get_project_settings().get('FILES_STORE')
#     def get_media_requests(self, item, info):
#         if isinstance(item, DownloadItem):
#             print("in file pipeline: ", type(item), item)
#             for url in item["file_url"]:
#                 time.sleep(1)
#                 yield scrapy.Request(url)
#         else:
#             return
#     def item_completed(self, results, item, info):
#         if isinstance(item, DownloadItem):
#             print("in file pipeline: ", type(item), item)
#             image_paths = [x['path'] for ok, x in results if ok]
#             # 定义分类保存的路径
#             #img_path = "%s/%s" % (self.file_store, item['title'])
#             img_path = self.file_store
#             # 目录不存在则创建目录
#             if os.path.exists(img_path) == False:
#                 os.makedirs(img_path)
#             for i in range(len(image_paths)):
#                 #if we got no multiple files, we can just use shutil.move()
#                 shutil.move(self.file_store + "\\" + image_paths[i], img_path + "\\" + item['title'][i])
#                 print("%s move successfully\n\n" %(img_path + "\\" + item["title"][i]))
#             return item
#         return

# class HtmlDownloadPipeline(FilesPipeline):
#     file_store = get_project_settings().get('FILES_STORE')
#     def get_media_requests(self, item, info):
#         if isinstance(item, DownloadHtml):
#             print("in html pipeline: ", type(item), item)
#             for url in item["file_url"]:
#                 # time.sleep(1)
#                 yield scrapy.Request(url)
#         else:
#             return
#     def item_completed(self, results, item, info):
#         if isinstance(item, DownloadHtml):
#             print("in html pipeline: ", type(item), item)
#             image_paths = [x['path'] for ok, x in results if ok]
#             img_path = self.file_store
#             # 目录不存在则创建目录
#             if os.path.exists(img_path) == False:
#                 os.makedirs(img_path)
#             for i in range(len(image_paths)):
#                 shutil.move(self.file_store + "\\" + image_paths[i], img_path + "\\" + item['title'][i] + ".html")
#                 print("%s move successfully\n\n" %(img_path + "\\" + item["title"][i]))
#             return item
#         return

class CrawlerPipeline(object):
    write_number = 0
    file_num = 0
    # if os.path.exists(os.path.join(DATA_STORE, "latest_file_num.txt")):
    #     with open(os.path.join(DATA_STORE, "latest_file_num.txt"), "r") as f:
    #         file_num = int(f.readline())
    for file_name in os.listdir(DATA_STORE):
        if "KernelInfo" in file_name:
            _ = file_name.split(".")[0]
            new_num = int(_.split("_")[1])
            file_num = new_num if new_num > file_num else file_num
            file_num += 1

    file_ = None
    exporter_ = None
    tmp_name = "tmp.json"
    tgt_name = "KernelInfo"

    def open_new_file(self):
        self.file_ = open(os.path.join(data_directory, self.tmp_name), 'wb')  # in some machines, we should use 'w'
        self.exporter_ = JsonItemExporter(self.file_, encoding='utf-8', ensure_ascii=False)
        self.exporter_.start_exporting()
        return

    def __init__(self):
        self.open_new_file()

    def close_spider(self, spider):
        self.exporter_.finish_exporting()
        self.file_.close()

        f = open(os.path.join(data_directory, self.tmp_name), 'r', encoding="utf-8")
        text = f.read()
        f.close()

        data = json.loads(text)

        target_json = self.tgt_name + "_%d" % (self.file_num) + ".json"
        f = open(os.path.join(data_directory, target_json), 'w')
        json.dump(data, f, sort_keys=True, indent=4)
        f.close()

        self.file_num += 1

        # with open(os.path.join(DATA_STORE, "latest_file_num.txt"), "w") as f:
        #     f.write("{}".format(self.file_num))

    def process_item(self, item, spider):
        if isinstance(item, FirstPageInfo):
            self.exporter_.export_item(item)
            self.write_number += 1
            if self.write_number >= MAX_TO_WRITE_IN_A_FILE:
                self.write_number = 0

                self.exporter_.finish_exporting()
                self.file_.close()

                f = open(os.path.join(data_directory, self.tmp_name), 'r', encoding="utf-8")
                text = f.read()
                f.close()

                data = json.loads(text)

                target_json = self.tgt_name + "_%d"%(self.file_num) + ".json"
                f = open(os.path.join(data_directory, target_json), 'w')
                json.dump(data, f, indent=4)#sort_keys=True,
                f.close()

                self.file_num += 1
                self.open_new_file()
        return item

# class CrawlerPipeline_each_page(object):
#     write_number = 0
#     file_num = 0
#
#     file = None
#     exporter = None
#     tmp_name = "tmp_each_page.json"
#     tgt_name = "DetailsOfKernel"
#
#     def open_new_file(self):
#         self.file = open(os.path.join(data_directory, self.tmp_name), 'wb')  # in some machines, we should use 'w'
#         self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
#         self.exporter.start_exporting()
#         return
#
#     def __init__(self):
#         self.open_new_file()
#
#     def close_spider(self, spider):
#         self.exporter.finish_exporting()
#         self.file.close()
#
#         f = open(os.path.join(data_directory, self.tmp_name), 'r', encoding="utf-8")
#         text = f.read()
#         f.close()
#
#         data = json.loads(text)
#
#         target_json = self.tgt_name + "_%d" % (self.file_num) + ".json"
#         f = open(os.path.join(data_directory, target_json), 'w')
#         json.dump(data, f, sort_keys=True, indent=4)
#         f.close()
#
#         self.file_num += 1
#
#     def process_item(self, item, spider):
#         if isinstance(item, EachPageInfo):
#             self.exporter.export_item(item)
#             self.write_number += 1
#             if self.write_number >= MAX_TO_WRITE_IN_A_FILE:
#                 self.write_number = 0
#
#                 self.exporter.finish_exporting()
#                 self.file.close()
#
#                 f = open(os.path.join(data_directory, self.tmp_name), 'r', encoding="utf-8")
#                 text = f.read()
#                 f.close()
#                 data = json.loads(text)
#
#                 target_json = self.tgt_name + "_%d"%(self.file_num) + ".json"
#                 f = open(os.path.join(data_directory, target_json), 'w')
#                 json.dump(data, f, sort_keys=True, indent=4)
#                 f.close()
#
#                 self.file_num += 1
#                 self.open_new_file()
#         return item
