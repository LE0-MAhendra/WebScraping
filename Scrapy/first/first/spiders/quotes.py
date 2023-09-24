import scrapy
import json


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/api/quotes?page=1"]

    def parse(self, response):
        json_res = json.loads(response.body)
        quotes = json_res.get('quotes')
        for quote in quotes:
            yield {
                'author': quote.get('author').get('name'),
                'tags': quote.get('tags'),
                'quote': quote.get('text'),
            }
        check_next = json_res.get('has_next')
        if check_next:
            next_page_number = json_res.get('page')+1
            yield scrapy.Request(
                url=f'https://quotes.toscrape.com/api/quotes?page={next_page_number}', callback=self.parse,
            )
