# -*- coding: utf-8 -*-
from scrapy import cmdline
import winsound, re, json, os

cmdline.execute('scrapy crawl AuthorAndDatasetSpider'.split())

# s = os.path.getsize('J:\\EECS_6414\\Data\\19-02-03\\test_pages\\author_pages\\ymuratsimsek.html')
# print(s)

# a = [i for i in range(47,56 + 1)]
# file_path = "J:\\EECS_6414\\Data\\19-02-03\\KernelInfo_{}.json"
# for json_path in a:
#     if not os.path.exists(file_path.format(json_path)):
#         continue
#     with open(file_path.format(json_path), "r") as j:
#         print(file_path.format(json_path))
#         kernels = json.load(j)

# def get_ajax_json(parameter, page_size):
#     # parameter is the parameter of json url.
#     # it looks like "&competition=9988"
#     import requests
#     num = 0
#     url = "https://www.kaggle.com/kernels.json?sortBy=hotness&group=everyone{}&pageSize={}".format(parameter,page_size)
#     next_url = url
#     while True:
#         r = requests.get(next_url,
#                          auth=('user', 'pass')).json()
#         if len(r) == 0:
#             break
#         elif len(r) > 0 and len(r) < page_size:
#             num += len(r)
#             break
#         else:
#             num += len(r)
#             last_id = r[len(r) - 1]["id"]
#             next_url = url + "&after={}".format(last_id)
#     return num
#
# b = get_ajax_json("&competitionId=9988", 200)
# print(b)



# a = [1, 2, 3, 3, None, 3, 3, 5, None, 5]
# for i in a:
#     if i == None:
#         a.remove(i)
# print(a)
