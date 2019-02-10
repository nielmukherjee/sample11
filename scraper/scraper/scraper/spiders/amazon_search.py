# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import numpy as np
import pandas as pd

#how to throttle /speed down scrapy
#email pass usrame
#profile page- .1 what do u prefer brandname or price 2 . does no of review atter
# 3 what is min rating when you select a product
# in database.py create prefrence table, user table # function
class AmazonSearchSpider(scrapy.Spider):
    name = 'amazon_search'
    allowed_domains = ['amazon.in']
    search_term = 'pans'
    base_url = 'https://www.amazon.in'
    search_url = base_url + '/' + search_term + '/s?ie=UTF8&page=1&rh=i%3Aaps%2Ck%3A' + search_term
    start_urls = [search_url]
    counter = 0

    def parse(self, response):
        items = response.css('#s-results-list-atf li')
        next = response.css('#pagnNextLink::attr(href)').extract_first()
        for product in items:
            product_link = product.css('a.s-access-detail-page::attr(href)').extract_first()
            if product_link:
                yield Request(product_link, self.parse_product)
            else:
                print('skipped')

        if next and self.counter < 5:
            self.counter += 1
            link = self.base_url + next
            print(f"next page ==> {link}")
            yield Request(link, self.parse)

    def parse_product(self, response):
        print(f"product page => {response.css('title::text').extract_first()}")
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
            brandname = response.css('#bylineInfo::text').extract_first( )
        except Exception as e:
             brandname = ""
        try :
            numberreviews= response.css("#acrCustomerReviewText::text").extract_first()
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
            'brand':brandname,
            'totalreviews':numberreviews,
        }
