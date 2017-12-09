# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from hexunpjt.items import HexunpjtItem


class CsdnbkSpider(scrapy.Spider):
    name = 'csdnbk'
    allowed_domains = ['csdn.net']
    wid='csdnnews'
    def start_requests(self):
        yield Request('http://blog.csdn.net/'+str(self.wid),headers=
    {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
   'Accept-Language':'zh-CN,zh;q=0.8',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
   'Connection':'keep-alive'
   })

    def parse(self, response):
        item=HexunpjtItem()
        t=response.xpath('//*[@id="article_list"]/div/div[1]/h1/span/a/text()').extract()
        ie=[]
        for i in range(len(t)):
            i1=str(t[i])
            ie.append(i1.strip())
        item['name']=ie
        item['url']=response.xpath('//*[@id="article_list"]/div/div[1]/h1/span/a/@href').extract()
        item['hits']=response.xpath('//*[@id="article_list"]/div/div[3]/span[2]/text()').extract()
        item['comment']=response.xpath('//*[@id="article_list"]/div/div[3]/span[3]/text()').extract()
        ye=response.xpath('//*[@id="papelist"]/span/text()').extract()
        ye1=response.xpath('//*[@id="papelist"]/strong/text()').extract()
        yield item
        ye=ye[0]
        if ye1[0]=='1':
            print('共计'+ye[0:4]+'条')
        ye=ye[8]
        #print(type(ye) )
        if ye >'1':
            for j in range(2,int(ye)+1):
                yield Request(url='http://blog.csdn.net/csdnnews/article/list/'+str(j),callback=self.parse,
                          headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'})



