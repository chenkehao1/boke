# -*- coding: utf-8 -*-
import pymysql
import codecs
import json
# Define your item pipelines here
#爬取和讯博客用户博文数据项目
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class HexunpjtPipeline(object):
    def __init__(self):
        #刚开始链接时对应的数据库
        self.f=codecs.open('D:/AuI18N/1.json','wb',encoding= 'utf-8')
    def process_item(self, item, spider):
        for j in range(0,len(item['name']) ):
            name=item['name'][j]
            url=item['url'][j]
            hits=item['hits'][j]
            comment=item['comment'][j]
            g={'name':name,'url':url,'hits':hits,'comment':comment}
            i=json.dumps(dict(g),ensure_ascii= False )
            h=i+'\n'
            self.f.write(h)
        return item
    def close_spider(self):
        self.f.close()


'''
#写入数据库代码
class HexunpjtPipeline(object):
    def __init__(self):
        #刚开始链接时对应的数据库
        self.f=pymysql.connect(host='127.0.0.1',user='root',passwd='root',db='hexun1')
    def process_item(self, item, spider):
        #每一个博文列表包含多篇博文信息，可以用for循环一次处理各博文信息
        for j in range(len(item['name'])):
            #将获取到的各类信息分别赋予变量
            name=item['name'][j]
            url=item['url'][j]
            hits=item['hits'][j]
            comment=item['comment'][j]
            sql="insert into myhexun1(name,url,hits,comment) VALUES('"+name+"','"+url+"','"+hits+"','"+comment+"')"
            self.f.query(sql) #通过对应的sql语句实现写入数据库
        return item
    def close_spider(self):
        self.f.cloae()
        '''
