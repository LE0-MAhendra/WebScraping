import scrapy


class WorldmeterSpider(scrapy.Spider):
    name = "worldmeter"
    allowed_domains = ["www.worldometers.info"]
    start_urls = [
        "https://www.worldometers.info/world-population/population-by-country"]

    def parse(self, response):
        # title = response.xpath('//h1/text()').get()
        countries = response.xpath('//td/a')
        for country in countries:
            country_name = country.xpath(".//text()").get()
            link = f"https://{self.allowed_domains[0]}{country.xpath('.//@href').get()}"
            yield response.follow(url=link, callback=self.parse_country, meta={'country': country_name})

    def parse_country(self, response):
        # headings = response.xpath(
        #     '//table[@class="table table-striped table-bordered table-hover table-condensed table-list"]/thead/tr/th/text()').extract()
        country = response.request.meta['country']
        rows = response.xpath(
            '(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr')
        data = {}
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()
            # yield {
            #     'country': country,
            #     'year': year,
            #     'population': population,
            # }
            if year is not None:
                data[year] = population
        yield {
            country: data
        }
