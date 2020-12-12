from lxml import etree
import json, re

with open("webpages.html", "r", encoding= "utf-8") as f:
    html = f.read()
page_source = etree.HTML(html)
_ = page_source.xpath("/html/body/div[2]/div[2]/script[1]/text()")[0]
p = re.compile("Kaggle\.State\.push\(\{[\s\S]*\}\)\;")
info = p.findall(_)[0].replace("Kaggle.State.push(", "")[0:-2]
item = json.loads(info)
print(item)
