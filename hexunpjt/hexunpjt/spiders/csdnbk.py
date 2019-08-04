import scrapy

from scrapy.http import Request
from hexunpjt.items import HexunpjtItem
import urllib.request
class CsdnbksSpider(scrapy.Spider):
    name = 'csdnbks'
    allowed_domains = ['csdn.net']
    wid='csdnnews'
    def start_requests(self):
        yield Request('http://blog.csdn.net/'+str(self.wid),headers=
        {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
})


    def parse(self, response):
        item=HexunpjtItem()
        #爬取博客主页信息
        a=response.xpath('//*[@id="aside"]/div[2]/div[3]/div/img/@src').extract()
        if len(a)==1:
            a=a[0]
            item['dj']=a[-9:-4]
            item['fwl']=response.xpath('//*[@id="aside"]/div[2]/div[2]/span[2]/text()').extract()
            item['pm']=response.xpath('//*[@id="aside"]/div[2]/div[4]/span[2]/text()').extract()
            item['jf']=response.xpath('//*[@id="aside"]/div[2]/div[5]/span[2]/text()').extract()
        #文章爬取循环
        for j in range(1,100):
            #网站是动态加载的，先捕捉到动态请求网址，然后验证页面是否有数据，有的话就爬取，没有就停止
            headers2=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36')]
            op=urllib.request.build_opener()
            op.addheaders =headers2
            urllib.request.install_opener(op)#将op安装为全局
            data=urllib.request.urlopen('http://blog.csdn.net/csdnnews/svc/getarticles?pageindex='+str(j)+'&pagesize=100' ).read()
            if len(data) !=0:
                yield Request(url='http://blog.csdn.net/'+str(self.wid)+'/svc/getarticles?pageindex='+str(j)+'&pagesize=100',
                            headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'})
                item['name']=response.xpath('/html/body/li/h3/a/text()').extract()
                item['url']=response.xpath('/html/body/li/h3/a/@href').extract()
                item['hits']=response.xpath('/html/body/li/div/div/div[3]/span/text()').extract()
                item['comment']=response.xpath('/html/body/li/div/div/div[4]/span/text()').extract()
                i=len(item['name'])
            else:
                if i!=0:print('第'+'共计'+str(i)+'篇文章')
                break

        yield item


