# -*- coding: utf-8 -*-
import scrapy
from proxy.items import ProxyItem
from scrapy.http import Request


class ProxyspiderSpider(scrapy.Spider):
    name = 'proxySpider'
    allowed_domains = ['www.xicidaili.com']
    start_urls = []
    for i in range(1, 611):
        start_urls.append('http://www.xicidaili.com/nt/'+str(i))

    def parse(self, response):
        # 爬取代理数据
        selector = response.xpath('//table[@id="ip_list"]/tr')

        items = []
        for index, sub in enumerate(selector):
            if index == 0:
                continue
            item = ProxyItem()
            td = sub.xpath('./td')
            if td:
                item['ip'] = td[1].xpath('./text()').extract()[0].strip('\t\r\n ')
                item['port'] = td[2].xpath('./text()').extract()[0].strip('\t\r\n ')
                t = td[3].xpath('./a/text()')
                if t:
                    item['location'] = t.extract()[0].strip('\t\r\n ')
                else:
                    item['location'] = ''
                item['type'] = td[4].xpath('./text()').extract()[0].strip('\t\r\n ')
                item['protocol'] = td[5].xpath('./text()').extract()[0].strip('\t\r\n ')
                items.append(item)

        # 爬取页码
        # page = response.xpath('//div[@class="pagination"]/a[@class="next_page"]/@href').extract()
        # print page
        # if len(page) > 0:
        #     if '/nt/2' != page[0]:
        #         yield Request("http://www.xicidaili.com" + page[0])
        # yield Request(urlparse.urljoin(response.url, url))
        # #Request()函数没有赋值给callback，就会默认回调函数就是parse函数，所以这个语句等价于
        # yield Request(urlparse.urljoin(response.url, url), callback=parse)
        return items
