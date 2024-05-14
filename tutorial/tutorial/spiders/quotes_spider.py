import scrapy
from urllib.parse import urlparse

class QuotesSpider(scrapy.Spider):
    name = 'QuotesSpider'
    
    def __init__(self, base_url='', *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.base_domain = urlparse(base_url).netloc
        self.start_urls = [base_url]

    def parse(self, response):
        # Extract text from the current page
        text = ''.join(response.xpath('//text()').getall()).strip()
        yield {
            'url': response.url,
            'text': text
        }

        # Follow all links on the page and parse recursively
        for next_page in response.css('a::attr(href)').getall():
            if not self.is_google_images_link(next_page):
                yield response.follow(next_page, callback=self.parse)

    def is_google_images_link(self, url):
        parsed_url = urlparse(url)
        return "google" in parsed_url.netloc and "imgres" in parsed_url.path
