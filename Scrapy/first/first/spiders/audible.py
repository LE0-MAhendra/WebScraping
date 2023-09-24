from typing import Iterable
import scrapy
from scrapy.http import Request


class AudibleSpider(scrapy.Spider):
    name = "audible"
    allowed_domains = ["www.audible.in"]
    start_urls = ["https://www.audible.in/search"]
    custom_settings = {
        'DOWNLOAD_DELAY': 1.0,  # 2-second delay between requests
    }

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse,
                             headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"})

    def parse(self, response):
        page = response.meta.get('page', 1)
        all_li = response.xpath('//li[contains(@class, "productListItem")]')
        for prod in all_li:
            title = prod.xpath('.//h3/a/text()').get()
            author = prod.xpath(
                './/li[contains(@class, "authorLabel")]//span//a/text()').get()
            time = prod.xpath(
                './/li[contains(@class, "runtimeLabel")]//span/text()').get()
            yield {
                'page': page,
                'title': title,
                'author': author,
                'time': time,
                'User-Agent': response.request.headers['User-Agent'],
            }
        pagination = response.xpath("//ul[contains(@class,'pagingElements')]")
        next = pagination.xpath(
            ".//span[contains(@class,'nextButton')]/a/@href").get()
        next_page_url = f"https://www.audible.in{next}"
        if next_page_url:
            page += 1
            yield response.follow(url=next_page_url, callback=self.parse, meta={'page': page}, headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"})
