import scrapy
from e04.items import E04Item
from scrapy_splash import SplashRequest
from scrapy.http import FormRequest
import logging
import re
class e04Spider(scrapy.Spider):
	name = "e04"
	start_url = 'https://www.104.com.tw/jobs/search/'
	def start_requests(self):
		queryStringList = [
			{
				'keyword':'python',
				'area':'6001001000',
			},
			{
				'keyword':'爬蟲',
				'area':'6001001000',
			},
			{
				'keyword':'python後端',
				'area':'6001001000',
			},
			{
				'keyword':'資料分析',
				'area':'6001001000',
			},
			{
				'keyword':'java工程師',
				'area':'6001001000',
			},
		]
		for queryString in queryStringList:
			yield FormRequest(url=self.start_url,method="GET",formdata=queryString,callback=self.detail_requests)
	def detail_requests(self,response):
		yield SplashRequest(response.request.url,self.deep_request,meta={'url':response.request.url},endpoint='render.html',dont_filter=True)
	def deep_request(self,response):
		url = response.meta.get('url')
		logging.info(url)
		html = response.text
		amount = int(re.findall('<meta.*－(.*?) 個工作機會.*',html)[0])
		page = int(amount / 20) + 1
		logging.info(page)
		for page in range(1,page+1):
			yield SplashRequest(url+"&page="+str(page),endpoint='render.html',dont_filter=True)
	def parse(self,response):
		html = response.text
		keyword = "".join(set([i.lower() if i.isalpha() else i for i in set(re.findall('<em.*?ht">(.*?)</em>',html))]))
		logging.info(keyword)
		logging.info("into parse function")
		jobs = response.xpath('//article/div[@class="b-block__left"]')
		logging.info(len(jobs))
		for job in jobs:
			item = E04Item()
			item['category'] = keyword
			item['name'] = job.css('a').re('.*get="_blank">(.*?)</a>')[0].replace('<em class="b-txt--highlight">','').replace('</em>','')
			item['jobLink'] = "http:" + job.css('a').re('.*href="(.*?)" class=.*')[0]
			item['company'] = job.xpath('./ul[1]/li/a/@title').get().split("：")[1].replace("\n公司住址","")
			item['companyAddress'] = job.xpath('./ul[1]/li/a/@title').get().split("：")[-1]
			item['companyLink'] = "http:" +  job.xpath('./ul[1]/li/a/@href').get()
			item['jobArea'] = job.xpath('./ul[2]/li[1]/text()').get()
			item['experience'] = job.xpath('./ul[2]/li[2]/text()').get()
			item['school'] = job.xpath('./ul[2]/li[3]/text()').get()
			item['description'] = job.xpath('./p/text()').get()
			item['salary'] = job.xpath('./div/span/text()').get()
			yield item