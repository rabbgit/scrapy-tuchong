# -*- coding: utf-8 -*-
import scrapy
from tuchong.items import TuchongItem
import re


class TuChongSpider(scrapy.Spider):
    name = 'tuchong'

    start_urls = ["https://tuchong.com/tags/%E7%BE%8E%E5%A5%B3/"]
    image_xpath = "//img/@src"
    next_url_xpath = "//div[contains(@class, 'pages')]/a/@href"
    item_list_xpath = "//a[@data-location='content']/@href"

    def parse(self, response):
        next_pages = response.xpath(self.next_url_xpath).extract()
        for url in next_pages:
            yield self.get_request(self.start_urls[0] + url)

        item_links = response.xpath(self.item_list_xpath).extract()
        for link in item_links:
            yield scrapy.Request(link, callback=self.parse_item)

    def get_request(self, url):
        return scrapy.Request(url)

    def parse_item(self, response):
        all_item = response.xpath(self.image_xpath).extract()
        image_list = []
        for url in all_item:
            # print "URL %s" % url
            if re.search('.jpg$', url):
                image_list.append(url)
        item = TuchongItem()
        item["image_urls"] = image_list
        yield item
