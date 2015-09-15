# -*- coding: utf-8 -*-
import scrapy
from leetSpider.items import LeetspiderItem
from scrapy.selector import Selector
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
        	difficulty = prob.xpath('td[@value]/text()').extract()
        	item['title'] = title
        	item['link'] =  ["https://leetcode.com" + ''.join(link)]
        	item['difficulty'] = difficulty
        	items.append(item)
    	return items

