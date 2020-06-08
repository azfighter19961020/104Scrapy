# 104Scrapy
# 使用scrapy爬取104人力銀行

> 使用scrapy_splash來對付動態加載，取工作筆數來計算頁數

# 檔案

spiders/e04Spider --> 爬蟲主檔 <br>
db.py --> 串接資料庫類(在pipeline引用) <br>
items.py --> 建立item Field <br>
pipelines.py --> 處理item存取 <br>
run.py --> 使用scrapy.cmdline執行爬蟲 <br>
settings.py --> 設定splash url以及middleware <br>

# 資料爬取效果

> 根據工作分為不同的資料庫

(img)
