SET PYTHONPATH=.
::scrapy crawl data5uCrawler

@echo off

:start
scrapy crawl data5uCrawler
choice /t 60 /d y /n >nul

goto start