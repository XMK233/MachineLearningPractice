# -*- coding: utf-8 -*-
from scrapy import cmdline
import winsound, re, json

cmdline.execute('scrapy crawl data5uCrawler'.split())

# a = [1,2,3,4]
# b = [2,3,4,5]
# c = [5,7,8,9]
# for q, w, e in zip(a, b, c):
#     print(q, w, e)

# import wget
# filename = wget.download('https://www.kaggle.com/ashishpatel26/genetic-algorithm-for-beginner')
# print(filename)

# from lxml import etree
# with open("J:\\EECS_6414\\Data\\19-01-29\\files\\ashishpatel26_genetic-algorithm-for-beginner.html", "r", encoding= "utf-8") as f:
#     #j = json.load(f)
#     t = f.readlines()
#     print(t)
#     tree = etree.HTML(t)
#     print(tree)
#     r = tree.xpath("//div[@id='comments']")
#     print(r)
#     pass

# from bs4 import BeautifulSoup
# path = "J:\\EECS_6414\\Data\\19-01-29\\files\\ashishpatel26_genetic-algorithm-for-beginner.html"
# htmlfile = open(path, 'r', encoding='utf-8')
# htmlhandle = htmlfile.read()
# soup = BeautifulSoup(htmlhandle, 'lxml')

# from lxml import html
# path = "J:\\EECS_6414\\Data\\19-01-29\\files\\ashishpatel26_genetic-algorithm-for-beginner.html"
# htmlfile = open(path, 'r', encoding='utf-8')
# htmlhandle = htmlfile.read()
# htmlfile.close()
# tree = html.fromstring(htmlhandle)
# print(htmlhandle)
# print(tree.xpath("/html[@class='gr__kaggle_com']/body/div[@class='site-layout']/div[@class='site-layout__main-content']/div/div/div[@class='sc-dGSLCc ccbWMk']/div[@class='kernel-viewer']/div[@class='kernel-viewer__container']/div[@id='kernel-viewer__pane-container']/div[@id='comments']/div[@class='comment-list']/div[7]/div[@id='435031']/div[@class='discussion-comment discussion-comment--parent']/div[@class='discussion-comment__body']/div[@class='discussion-comment__replies']/div[@class='discussion-comment__linking-line']/div[2]/div[@id='441723']/div[@class='discussion-comment']/div[@class='discussion-comment__body']/div[@class='discussion-comment__content']/div[@class='markdown-converter__text--rendered']/p[1]/text()"))

# f = open("C:\\Users\\xmk233\\Desktop\\js1.txt")
# text = f.read()
# print(text)
# p = re.compile("Kaggle\.State\.push\(\{[\s\S]*\}\)\;")
# y = p.findall(text)[0].replace("Kaggle.State.push(", "")[0:-2]
# print(y)
# j = json.dumps(y)
# print(j)
# f.close()

