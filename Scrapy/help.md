# Starting

creation of project

```bash
scrapy startproject Projectname
#or
scrapy startproject Projectname . #for making it one file
```

# Run the command to start a spider to scrape a website

```bash
scrapy genspider nameofwebsite websiteLink

#the website link must be in the form of www.google.comm
#dont use any prefix like http: or https: and suffix like / at end

#Example
scrapy genspider google www.google.com
```

After running the commmand we can see the file is been created in spider folder with the website name given in command

## Use Scrapy shell

```bash
scrapy shell

res=scrapy.Request(url='https://www.google.com')
fetch(res)
#It loads all data and checks the link
#use xpath for data fetch
response.xpath('//h1/text()').get() # it gives the title
# for multiple names
response.xpath('//td/a/text()').getall()
#links
response.xpath('//td/a/@href').getall()
```

## Running the Scripts in newly created file

using all the xpaths and values into the file and run it

```bash
import scrapy


class WorldmeterSpider(scrapy.Spider):
    name = "worldmeter"
    allowed_domains = ["www.worldometers.info"]
    start_urls = [
        "https://www.worldometers.info/world-population/population-by-country"]

    def parse(self, response):
        title = response.xpath('//h1/text()').get()
        countries = response.xpath('//td/a/text()').getall()
        yield {
            'titles': title,
            'countries': countries,
        }

```

# Run the Program

```bash
scrapy crawl filename
```

# saving the file

```bash
scrapy crawl filename name.json/name.csv
```

# change the user agent

during scraping the browser knows the scrapy is activated
we can verify it going in to scrapy shell
run the command requests.headers

b'User-Agent': [b'Scrapy/2.11.0 (+https://scrapy.org)']

# Need to make a new user agent in settings or in code file

In settings

DEFAULT*REQUEST_HEADERS = { # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/\_;q=0.8", # "Accept-Language": "en",
'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
}

or

make a new function in the class of the file

````bash
def start_requests(self):
    yield scrapy.Request(url=self.start_urls[0], callback=self.parse,
    headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"})

# if there are multiple pages

if next_page_url:
    yield response.follow(url=next_page_url, callback=self.parse, meta={'page': page}, headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"})
    ```
````

# Usage of CrawlSpider

```bash
scrapy genspider -t crawl filename
```

# example code for Crawl spider

```bash
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class TranscriptsSpider(CrawlSpider):
    name = 'transcripts'
    allowed_domains = ['subslikescript.com']
    # start_urls = ['https://subslikescript.com/movies_letter-X']

    # Setting an user-agent variable
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'

    # Editing the user-agent in the request sent
    def start_requests(self):
        yield scrapy.Request(url='https://www.google.co', headers={
            'user-agent': self.user_agent
        })

    # Setting rules for the crawler
    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//ul[@class='scripts-list']/a")),
             callback='parse_item', follow=True, process_request='set_user_agent'),

        ## Link extractors are used for entering into link and get the data
        #main link should be first
        # make the next links in this
        Rule(LinkExtractor(restrict_xpaths=(
            "(//a[@rel='next'])[1]")), process_request='set_user_agent'),
    )

    # Setting the user-agent
    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request
     def parse_item(self, response):
        yield response.....
```

## Storing of values to DataBases

Go to settings and make changes to pipelines

Uncomment this

<!-- ITEM_PIPELINES = {
"first.pipelines.FirstPipeline": 300,
} -->

ITEM_PIPELINES = {
"first.pipelines.FirstPipeline": 300,
}
add functions to pipes like open and close

```bash
from itemadapter import ItemAdapter
import logging


class FirstPipeline:
    def open_spider(self, spider):
        logging.warning('Spider Opened - Pipeline')

    def close_spider(self, spider):
        logging.warning('Spider Closed - Pipeline')

    def process_item(self, item, spider):
        return item

```

## USe Splash for js driven websites with scrapy

first add a environment in docker for splash

first open cmd

```bash
docker pull scrapinghub/splash
```

now open doker environment and run where we made a container

as we run we can see a code runner at right

select a website and run the code

```bash
function main(splash, args)
    splash.private_mode_enabled = false
    assert(splash:go(args.url))
    assert(splash:wait(3))
    all_matches = assert(splash:select_all("label.btn.btn-sm.btn-primary"))
    all_matches[2]:mouse_click()
    assert(splash:wait(3))
    splash:set_viewport_full()
    return {splash:png(), splash:html()}
end
```

now we need to use splash with scrapy

```bash
pip install scrapy_splash
```

make changes to settings first

```bash
SPLASH_URL = 'http://localhost:8050'

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
```

```bash
# add script and change start_requests
script = '''
    function main(splash, args)
        splash.private_mode_enabled = false
        assert(splash:go(args.url))
        assert(splash:wait(3))
        all_matches = assert(splash:select_all("label.btn.btn-sm.btn-primary"))
        all_matches[2]:mouse_click()
        assert(splash:wait(3))
        splash:set_viewport_full()
        return {splash:png(), splash:html()}
    end
'''

# Define a start_requests function to connect scrapy and splash
def start_requests(self):
    yield SplashRequest(url='https://www.adamchoi.co.uk/overs/detailed', callback=self.parse,
                        endpoint='execute', args={'lua_source':self.script})
```
