## 关于获得每一个模型的json数据
from each page, please see this xpath: 

/html/body/div[2]/div[2]/script[1]/text()

用正则表达式取得Kaggle.State.push();之间的内容。

## 关于这个项目
如果你要新增一点啥，注意下述的
typical working pipeline: 
* items.py --> spiders --> pipelines.py --> settings.py

##关于爬虫

###2019年1月23日
目前最新的爬虫是DownloadCode.py

###2019年1月29日
CoarseSpider.py爬虫的功能和DownloadCode.py差不多。后者只是多了一个
简易的parse部分罢了，除此之外都一样。

### 2019年1月30日
使用wget来获取文件。scrapy的下载功能好像有点问题，总是下载不到正确的代码文件。最后
退而求其次，只能用别的库来获取文件了。

## 爬虫使用的requirement：
selenium, phantomJS, chromedriver, 
python 3.6(版本非常关键), 
scrapy 1.5，
wget (下载文件用的library)

## 使用说明：
中断后，找最后一个存下来的KernelInfo_x.json，这个文件在写入的时候没有排序，
所以咱干脆就去找最后一个kernel的ID然后写到代码里面去，重新运行就好。这一
部分我没有实现自动化，但就先这样吧。

## 使用日记
关掉了download的pipeline，以后要用的话就开启。
目前暂时不使用SimplifiedSpider.py.目前使用EvenSimplified.py这个爬虫只获取kernel的
metadata，并保存在19-02-19里面。

## IPCralwers.py
这个爬虫是用来获取ip地址的。