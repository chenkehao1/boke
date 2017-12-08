# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from hexunpjt.items import HexunpjtItem


class CsdnbkSpider(scrapy.Spider):
    name = 'csdnbk'
    allowed_domains = ['csdn.net']
    wid='csdnnews'
    def start_requests(self):
        yield Request('http://blog.csdn.net/csdnnews',headers=
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    })

    def parse(self, response):
        item=HexunpjtItem()
         item['name']=response.xpath('/html/body/li/h3/a/text()').extract()
        item['url']=response.xpath('/html/body/li/h3/a/@href').extract()
        item['hits']=response.xpath('/html/body/li/div/div/div[3]/span/text()').extract()
        item['comment']=response.xpath('/html/body/li/div/div/div[4]/span/text()').extract()

        for j in range(2,100):
            #print('共计有'+j)
            yield Request(url='http://blog.csdn.net/csdnnews/svc/getarticles?pageindex='+str(j)+'&pagesize=100',callback=self.parse,
                          headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'})
        yield item






