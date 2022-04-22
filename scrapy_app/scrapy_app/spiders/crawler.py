# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.spiders import CrawlSpider

from .. import items


class CrawlerSpider(CrawlSpider):
    name = 'crawler'

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.allowed_domains = [self.domain]
        self.category_dict = {
            'MapleStory Inventory Maple Wish Board': 1,
            'MapleStory Inventory Free Bulletin Board': 2,

        }

    def start_requests(self):
        for i in range(1, 2):  # go page by page
            yield scrapy.Request(self.url + str(i), self.parse_board)

    def parse_board(self, response):  # Get all posts on a page
        board = response.xpath('//tr[contains(@class, "ls") and contains(@class, "tr")]')

        for i in range(len(board)):
            # Access the href of the post on each page and get the title, content, number of recommendations, and views
            self.post_url = response.xpath('//tr[contains(@class, "ls") and contains(@class, "tr")]/td[@class="bbsSubject"]/a[@class="sj_ln"]/@href')[i].extract()
            yield scrapy.Request(self.post_url, self.parse_post)

    def get_num(self, s):
        regex = re.compile(r'\d{1,3}[,{1}\d{3}]*')
        num = regex.search(s)
        start, end = list(num.span())[0], list(num.span())[1]
        s = s[start:end]
        s_list = s.split(',')
        result = ''
        for n in s_list:
            result += n
        return int(result)

    def get_str(self, s_list):
        result = ''
        for s in s_list:
            result += s
        return result

    def parse_post(self, response):
        item = items.ScrapyAppItem()
        item['title'] = response.xpath('//*[@id="tbArticle"]/div[3]/div[1]/div[1]/h1/text()')[0].extract()
        item['contents'] = self.get_str(response.xpath('//*[@id="imageCollectDiv"]//div/text()|'
                                                       '//*[@id="imageCollectDiv"]//font/text()|'
                                                       '//*[@id="imageCollectDiv"]//p/text()|'
                                                       '//*[@id="imageCollectDiv"]//span/text()|'
                                                       '//*[@id="imageCollectDiv"]//strong/text()').extract())
        item['published_date'] = response.xpath('//*[@id="tbArticle"]/div[1]/div/div[2]/text()')[0].extract()
        item['views'] = self.get_num(response.xpath('//*[@id="tbArticle"]/div[1]/div/div[3]/text()')[1].extract())
        item['recommends'] = response.xpath('//*[@id="bbsRecommendNum1"]/text()')[0].extract()
        item['url'] = response.xpath('//*[@id="viewUrl"]/text()')[0].extract()
        category = response.xpath('//div[@class="viewTopBoardName"]/a/text()')[0].extract()
        for k, v in self.category_dict.items():
            if k == category:
                item['category'] = v

        yield item
