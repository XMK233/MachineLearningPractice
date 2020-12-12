# -*- coding: utf-8 -*-

with open("Ashish Patel(阿希什) _ Kaggle.html", "r", encoding= "utf-8") as f:
    html = f.read()

xpaths = {

}

from lxml import etree
import json, re
page_source = etree.HTML(html)
_ = page_source.xpath("/html/body/div[2]/div[2]/script[1]/text()")[0]
