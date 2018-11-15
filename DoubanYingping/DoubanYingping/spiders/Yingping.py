from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from DoubanYingping.items import DoubanyingpingItem
import os
import scrapy
import json
import time


class Getfilmurls(scrapy.Spider):
    name = 'getfilmurls'
    base_url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=&start='

    def start_requests(self):
        # 在这里设置抓取页数
        for i in range(0, 2):
            url = self.base_url + str(i*20)
            yield scrapy.Request(url, callback=self.get_urls)

    def get_urls(self, response):
        data = json.loads(response.text)
        # with open('./urls.txt', 'a+') as f:
        #     for film in data['data']:
        #         url = film['url']
        #         f.write(url+'\n')
        for film in data['data']:
            url = film['url']
            os.system('scrapy crawl yingping -a start_urls=' + url.strip())

class Yingping(CrawlSpider):
    name = 'yingping'
    rules = [
        Rule(LinkExtractor(allow=r"/subject/\d+/reviews$")),
        Rule(LinkExtractor(allow=r"/subject/\d+/reviews\?start=\d+$")),
        Rule(link_extractor=LinkExtractor(allow=r"review/\d+/"), callback="get_yingping", follow=False)
        ]
    num = 1

    def __init__(self, start_urls=None, *args, **kwargs):
        super(Yingping, self).__init__(*args, **kwargs)
        self.start_urls = [''.join(start_urls)]
        print(self.start_urls)

    def get_yingping(self, response):
        item = DoubanyingpingItem()
        title = response.xpath('//div[@class="article"]/h1/span/text()').extract()[0]
        date = response.xpath('//header[@class="main-hd"]/span[@class="main-meta"]/text()').extract()[0]
        author = response.xpath('//header[@class="main-hd"]/a')[0].xpath('string(.)').extract()[0].replace('\n', '').strip()
        filmname = response.xpath('//header[@class="main-hd"]/a[2]/text()').extract()[0]
        content = ''
        li = response.xpath('//div[@class="review-content clearfix"]/p')
        for i in li:
            content += i.xpath('string(.)').extract()[0]+'\n'
        item['title'] = title
        item['date'] = date
        item['author'] = author
        item['content'] = content
        item['filmname'] = filmname
        yield item
        print(self.num)
        self.num += 1




