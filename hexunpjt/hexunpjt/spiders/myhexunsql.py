# -*- coding: utf-8 -*-
import scrapy
import re
import urllib.request
from hexunpjt.items import HexunpjtItem
from scrapy.http import Request

# <div class='Article'><div class='ArticleTitle'><span class='ArticleTitleText'><span style='text-decoration:none; cursor:pointer' id='imgnext_111757611'></span><a href='http://fjrs168.blog.hexun.com/111757611_d.html'>如何避免一买就套一卖就涨</a></span>
#//span[@class='ArticleTitleText']/a/text()文章名的xpath表达式
#//span[@class='ArticleTitleText']/a/@heef

#评论数阅读数的字段('click111757611','760');$('comment111757611','0')
#'click\d*?','(\d*?)'#阅读数的正则
#'comment\d*?','(\d*?)'评论数的正则

#获取阅读数和评论数的请求地址和正则
#<script type="text/javascript" src="http://click.tool.hexun.com/linkclick.aspx?blogid=19020056&articleids=111757611-111741870-111699309-111682931-111667053-111651358-111626307-111595373-111580691-111565747-111757611-111741870-111699309-111682931-111667053-111651358-111626307-111595373-111580691-111565747"></script>
#<script type="text/javascript" src="(http://click.tool.hexun.com/.*?)">

#文章页数的地址
#http://27636918.blog.hexun.com/p1/default.html

#获取博客总页数的正则表达式href='http://fjrs168.blog.hexun.com/p58/default.html
#blog.hexun.com/p(\d*?)/    http://'+str(self.uid)+'.blog.hexun.com/p1/default.html
class MyhexunsqlSpider(scrapy.Spider):
    name = 'myhexunsql'
    uid='27636918'
    allowed_domains = ['hexun.com']
    #start_urls = ['http://hexun.com/']
    def start_requests(self):
        yield Request('http://fjrs168.blog.hexun.com/p1/default.html',headers=
    {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
   'Accept-Language':'zh-CN,zh;q=0.8',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
   'Connection':'keep-alive'
   })

    def parse(self, response):
        item=HexunpjtItem()
        item['name']=response.xpath("//span[@class='ArticleTitleText']/a/text()").extract()
        item['url']=response.xpath("//span[@class='ArticleTitleText']/a/@href").extract()
        #接下来需要用urllib和re模块获取博文的评论数和阅读数
        #首先提取储存评论数和点击数的正则
        pat1='<script type="text/javascript" src="(http://click.tool.hexun.com/.*?)">'#提取储存评论数和点击数的网址的正则表达式
        hcurl=re.compile(pat1).findall(str(response.body))[0]#获取到储存评论数和点击数的网址并保存给变量
        print(hcurl )
        #模拟成浏览器
        headers2=[('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
                  ( 'Accept-Language','zh-CN,zh;q=0.8'),
                    ('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'),
                  ('Connection','keep-alive')]
        op=urllib.request.build_opener()
        op.addheaders =headers2
        urllib.request.install_opener(op)#将op安装为全局
        data=urllib.request.urlopen(hcurl ).read()#爬取对应博客列表页的所有博文的点击数和评论数的数据
        #print(data)
        pat2="'click\d*?','(\d*?)'"#提取阅读数的正则
        pat3="'comment\d*?','(\d*?)'"#提取评论数的正则
        #获取阅读数和评论数的正则匹配
        item['hits']=re.compile(pat2).findall(str(data))
        item['comment']=re.compile(pat3).findall(str(data))
        yield item
        pat4='blog.hexun.com/p(\d*?)/'
        ye=re.compile(pat4).findall(str(response.body))
        if (len(ye)>=2):
            t=ye[-2]
        else:
            t=1
        print('共计'+str(t)+'页')
        for i in range(2,int(t)+1):
            url1='http://fjrs168.blog.hexun.com/p'+str(i)+'/default.html'
            yield Request(url1,callback=self.parse,
                          headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'})
