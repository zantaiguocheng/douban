# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
import re
from douban.items import DoubanItem

class DsSpider(CrawlSpider):
    name = 'ds'
    allowed_domains = ['read.douban.com']
    start_urls = ['https://read.douban.com/ebooks/']
    rules = (
        # Rule(LinkExtractor(allow=r'\d+',deny='\d+.+'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'\d+',deny='\d+.+'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'read.douban.com/kind/\d+\??'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        items=DoubanItem()
        x=Selector(response)
        lb=x.xpath('//div[@class="hd"]/h1/text()').extract()[0]
        zz_yz=x.re('作者</span.*?</a></span></span></p>')
        x_k=x.xpath('//div[@class="info"]')
        sm=x_k.xpath('./div[@class="title"]/a/text()').extract()
        jj=x_k.xpath('./div[@class="article-desc-brief"]/text()').extract()
        for i in range(len(sm)):
            items['lb']=lb
            items['sm']=sm[i]
            zz_k=re.findall('作者</span.*?</a></span></span>',zz_yz[i])
            items['zz']=re.findall('([〕〔\u4e00-\u9fa5·\s]{2,})',zz_k[0])[1:]
            yz_k=re.findall('译者</span.*?</a></span></span>',zz_yz[i])
            if not yz_k:
                items['yz']=None
            else:
                items['yz']=re.findall('([〕〔\u4e00-\u9fa5·]+)',yz_k[0])[1:]
            pf=x_k[i].xpath('./div/span[@class="rating-average"]/text()').extract()
            if not pf:
                items['pf']=None
            else:
                items['pf']=pf[0]
            items['jj']=jj[i]
            yield items
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
