# -*- coding: utf-8 -*-
import scrapy
from gxstnu.items import GxstnuItem


class XinwenSpider(scrapy.Spider):
    name = 'xinwen'
    # allowed_domains = ['http://www.gxstnu.edu.cn']
    # 开始爬取的url地址
    start_urls = [
        # 'http://quotes.toscrape.com/page/1/',
        # 'http://quotes.toscrape.com/page/2/',
        # 'http://quotes.toscrape.com/',
        'http://www.gxstnu.edu.cn/xxxw.htm',
    ]

    def parse(self, response):
        # 获取每个新闻的url
        title_urls = response.css('div.list_box ul li  a')
        yield from response.follow_all(title_urls, self.parse_news)

        # 获取下一页的url
        pagination_links = response.css('span.p_next a')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_news(self, response):
        # 使用css提取页面内容
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'title': extract_with_css('h1.c-title::text'),
            'others': extract_with_css('div.other-s::text'),
            'v_news_content': response.css('div.v_news_content p::text').getall(),
            'url': response.url,
        }

    # def parse(self, response):
    #     author_page_links = response.css('.author + a')
    #     yield from response.follow_all(author_page_links, self.parse_author)
    #
    #     pagination_links = response.css('li.next a')
    #     yield from response.follow_all(pagination_links, self.parse)
    #
    # def parse_author(self, response):
    #     def extract_with_css(query):
    #         return response.css(query).get(default='').strip()
    #
    #     yield {
    #         'name': extract_with_css('h3.author-title::text'),
    #         'birthday': extract_with_css('.author-born-date::text'),
    #         'bio': extract_with_css('.author-description::text'),
    #     }



    # def parse(self, response):
    #
    #     for quote in response.css('div.quote'):
    #         yield {
    #             'text': quote.css('span.text::text').get(),
    #             'author': quote.css('small.author::text').get(),
    #             'tags': quote.css('div.tags a.tags::text').get(),
    #         }
    #
    #     yield from response.follow_all(css='ul.pager a', callback=self.parse)