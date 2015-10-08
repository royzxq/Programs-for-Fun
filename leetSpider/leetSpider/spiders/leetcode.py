# -*- coding: utf-8 -*-
import scrapy
from leetSpider.items import LeetspiderItem
from scrapy.selector import Selector
import string
from tool import replace

class LeetcodeSpider(scrapy.Spider):
    name = "leetcode"
    allowed_domains = ["leetcode.com"]
    start_urls = [
        'https://leetcode.com/problemset/algorithms/'
    ]

    def parse(self, response):
        sel = Selector(response)
        prob_lists = sel.xpath("//table[@id='problemList']/tbody/tr")
        items = []

        for prob in prob_lists:
            item = LeetspiderItem()

            title = prob.xpath('td/a/text()').extract()
            link = prob.xpath('td/a/@href').extract()
            # link = "https://leetcode.com" + ''.join(link)
            # title = ''.join(title)
            link = response.urljoin(''.join(link))
            difficulty = prob.xpath('td[@value]/text()').extract()
            item['title'] = title[0].strip().replace(' ','_')
            item['link'] = link
            item['difficulty'] = difficulty[0]
            item['source'] = self.name
            yield scrapy.Request(link, callback=self.parse_content, meta={'item':item})
            
            # item['content'] = request.body
            # items.append(item)
        # return items

    def parse_content(self, response):
        sel = Selector(response)
        content = sel.xpath("//div[@class='question-content']/p")
        tags = sel.xpath("//div[@class='question-content']//div[@id='tags']/following-sibling::span/a/text()").extract()
        related = sel.xpath("//div[@class='question-content']//div[@id='similar']/following-sibling::span/a/text()").extract()
        item = response.meta['item']
        
        for i in xrange(len(related)):
            related[i] = replace(related[i]).strip().replace(' ','_')
            
        item['content'] = []
        item['tags'] = tags
        item['related'] = related

        for des in content:
            text = des.extract()
            if 'Credits' in text or 'style' in text or 'show hint' in text:
                continue
            if text:
                # text = replace(text)
                if text:
                    item['content'].append(text)
        # response.meta['content'] = item['content']
        return item


