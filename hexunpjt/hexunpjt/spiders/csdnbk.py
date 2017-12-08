# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from hexunpjt.items import HexunpjtItem
#文章标题的xpath表达式
#爬了知乎 200 万数据，图说程序员都喜欢去哪儿工作
#//*[@id="article_list"]/div/div[1]/h1/span/a/text()

#文章链接表达式，这里的文章链接需要进行字符串拼接，http://blog.csdn.net + /csdnnews/article/details/78712170
# <span class="link_title"><a href="/csdnnews/article/details/78712170">
#//*[@id="article_list"]/div/div[1]/h1/span/a/@href

#文章阅读数表达式
#<span class="link_view" title="阅读次数"><a href="/csdnnews/article/details/78712170" title="阅读次数">阅读</a>(35)</span>
#'//*[@id="article_list"]/div/div[3]/span[2]/text()

#评论数表达式
# <span class="link_comments" title="评论次数"><a href="/csdnnews/article/details/78712170#comments" title="评论次数" onclick="_gaq.push(['_trackEvent','function', 'onclick', 'blog_articles_pinglun'])">评论</a>(0)</span>
#//*[@id="article_list"]/div/div[3]/span[3]/text()

#页数网址
#http://blog.csdn.net/csdnnews/article/list/1....2...3

#博客访问、积分、等级、排名数表达式
#'//*[@id="blog_rank"]/li[1]/span/text()'#访问
#'//*[@id="blog_rank"]/li[2]/span/text()#积分

#<img src="http://c.csdnimg.cn/jifen/images/xunzhang/jianzhang/blog6.png"
#'//*[@id="blog_rank"]/li[3]/span/img/@src'#获取等级的表达式，这里等级是个图片，所要先拿图片网址在把里面的等级数提取出来
#'//*[@id="blog_rank"]/li[4]/span/text()#排名

#总页数和总条数表达式
#<span> 103条  共7页</span>
#'//*[@id="papelist"]/span/text()'
class CsdnbkSpider(scrapy.Spider):
    name = 'csdnbk'
    allowed_domains = ['csdn.net']
    wid='csdnnews'
    def start_requests(self):
        yield Request('http://blog.csdn.net/csdnnews',headers=
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

        yield item
        ye=ye[0]
        ye=ye[8]
        #print(type(ye) )
        if ye >'1':js=ye

        for j in range(2,int(js)):
            yield Request(url='http://blog.csdn.net/csdnnews/article/list/'+str(j),callback=self.parse,
                          headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'})







