# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import numpy as np
from time import sleep
import pandas as pd


# how to throttle /speed down scrapy
# email pass usrame
# profile page- .1 what do u prefer brandname or price 2 . does no of review atter
# 3 what is min rating when you select a product
# in database.py create prefrence table, user table # function
class AmazonSearchSpider(scrapy.Spider):
    name = 'amazon_search'
    allowed_domains = ['amazon.in']
    search_term = 'mobiles'
    base_url = 'https://www.amazon.in'
    counter = 0
    linknos = 0


    def __init__(self, search_term='mobiles', name="amazon_search", **kwargs):
        search_url = f'{self.base_url}/{search_term}/s?ie=UTF8&page=1&rh=i%3Aaps%2Ck%3A{search_term}' 
        self.start_urls = [search_url]
        super().__init__(name, **kwargs)

    def parse(self, response):
        items = response.css('#s-results-list-atf > li')
        next = response.css('#pagnNextLink::attr(href)').extract_first()
        for product in items:
            product_link = product.css('.s-item-container .s-access-detail-page::attr(href)').extract_first()
            if product_link and 'http' in product_link and '/gp' not in product_link:
                print(self.counter, self.linknos, product_link)
                self.linknos += 1
                yield Request(product_link, self.parse_product)

        if next and self.counter < 100:
            self.counter += 1
            link = self.base_url + next
            yield Request(link, self.parse)

    def parse_product(self, response):
        # print(f"\t\t\nproduct page => {response.css('title::text').extract_first()}")
        title = response.css("#productTitle::text").extract_first().replace('\n', '').strip()
        company = response.css("#bylineInfo::text").extract_first()
        customerreviews = response.css(".arp-rating-out-of-text::text").extract_first()
        try:
            rating = response.css("#acrPopover::attr(title)").extract_first().split()[0]
        except Exception as e:
            rating = np.nan
        try:
            reviews = response.css("#acrCustomerReviewText::text").extract_first().split()[0]
            reviews = reviews.replace(',', '')
            reviews = int(reviews)
        except Exception as e:
            reviews = np.nan
        try:
            price = response.css('#priceblock_ourprice::text').extract_first()
        except Exception as e:
            price = np.nan
        try:
            primaryprice = response.css('.currencyINR::text').extract_first().strip()
        except Exception as e:
            primaryprice = np.nan
        try:
            brandname = response.css('#bylineInfo::text').extract_first()
        except Exception as e:
            brandname = ""
        try:
            numberreviews = response.css("#acrCustomerReviewText::text").extract_first()
        except Exception as e:
            numberreviews = ""

        yield {
            'title': title,
            'price': price,
            'reviews': reviews,
            'rating': rating,
            'company': company,
            'customerreviews': customerreviews,
            'primaryprice': primaryprice,
            'brand': brandname,
            'totalreviews': numberreviews,
        }
