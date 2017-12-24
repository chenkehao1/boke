# -*- coding: utf-8 -*-
#https://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E9%9D%92%E5%B2%9B&kw=python&sm=0&p=1
import scrapy
import urllib.parse
from scrapy.http import Request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import re
import urllib.request
from qiouzhi.items import  QiouzhiItem
class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = ['zhaopin.com']
    cs=urllib.parse.quote('选择地区')#如果要找全国就输‘选择地区’
    gz=urllib.parse.quote('python')
    y=1
    headers= {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
   'Accept-Language':'zh-CN,zh;q=0.8',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
   'Connection':'keep-alive'
   }
    url='https://sou.zhaopin.com/jobs/searchresult.ashx?jl='+cs+'&kw='+gz+'&sm=0&p='

    def start_requests(self):
        yield Request(url=self.url+str(1),headers= self.headers)
   # start_urls = ('https://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E9%9D%92%E5%B2%9B&kw=python&sm=0&p=1')
    def parse(self,response):
        item=QiouzhiItem()
        '''
        a=response.xpath('/html/body/div[3]/div[3]/div[1]/span/em/text()').extract()
        print('爬取的条数'+str(a),a)'''

        headers2=[('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
        ( 'Accept-Language','zh-CN,zh;q=0.8'),
        ('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'),
        ('Connection','keep-alive')]
        op=urllib.request.build_opener()
        op.addheaders =headers2
        urllib.request.install_opener(op)#将op安装为全局
        data=urllib.request.urlopen(self.url+str(self.y)).read().decode('utf-8')

        par8='this,event,(..?)'#页数
        par1='href="http://jobs.zhaopin.com/.*?htm" target="_blank">(.*?)</a>'#职位
        par2='<td class="gsmc"><a href=".*?" target="_blank">(.*?)</a>'#公司
        par3='href="(http://jobs.zhaopin.com/.*?htm)"'#url
        par4='<td class="zwyx">(.*?)</td'#薪酬
        par5='<td class="gxsj"><span>(.*?)</span>'#时间
        par6='<td class="gzdd">(.*?)</td>'#地点
        par7='<li class="newlist_deatil_two"><span>.*?</span><span>(.*?)</span><span>(.*?)</span><span>(.*?)</span>'#<span>(.*?)</span>#摘要

        e=re.compile(par8).findall(data)
        item['zc']=re.compile(par1).findall(str(data))
        item['gs']=re.compile(par2).findall(str(data))
        item['url']=re.compile(par3 ).findall(str(data))
        item['xc']=re.compile(par4 ).findall(str(data))
        item['sj']=re.compile(par5 ).findall(str(data))
        item['dd']=re.compile(par6).findall(str(data))
        item['zy']=re.compile(par7).findall(str(data))

        yield item

        for i in range(2,int(e[0])+1):
            self.y=i
            yield Request(url=self.url+str(i),callback=self.parse, headers= self.headers)











