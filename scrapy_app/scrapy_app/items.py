# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyAppItem(scrapy.Item):
    unique_id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    contents = scrapy.Field()
    published_date = scrapy.Field()
    views = scrapy.Field()
    recommends = scrapy.Field()
    date = scrapy.Field()
    category = scrapy.Field()
    pass

class ProductItem(scrapy.Item):
    unique_id = scrapy.Field()
    market = scrapy.Field()
    amazon_url = scrapy.Field()
    product_name = scrapy.Field()
    list_price = scrapy.Field()
    currency_symbol = scrapy.Field()
    save_price = scrapy.Field()
    save_in_percentage = scrapy.Field()
    main_image = scrapy.Field()
    ratings_total = scrapy.Field()
    availability = scrapy.Field()
    is_prime = scrapy.Field()
    affiliate_link = scrapy.Field()
    is_new = scrapy.Field()
    is_sold_by_amazon = scrapy.Field()
    is_sold_by_third_party = scrapy.Field()
    category = scrapy.Field()
    pass
