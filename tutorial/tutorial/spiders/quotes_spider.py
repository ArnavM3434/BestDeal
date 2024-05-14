import scrapy
from urllib.parse import urljoin, urlparse

links = 0

class QuotesSpider(scrapy.Spider):
    name = 'bestdeal'

    def __init__(self, base_url='', *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.base_url = base_url
        self.start_urls = [base_url]

    def parse(self, response):
        # Extract text from the current page
        global links
        text = ''.join(response.xpath('//text()').getall()).strip()
        yield {
            'url': response.url,
            #'text': text
        }

        # Follow all links on the page and parse recursively
        for next_page in response.css('a::attr(href)').getall():
            #full_next_page_url = self.get_full_url(response.url, next_page)
            if next_page and links < 100:
                links += 1
                yield response.follow(next_page, callback=self.parse)

    def get_full_url(self, current_page_url, next_page):
        if next_page.startswith('http://') or next_page.startswith('https://'):
            # Absolute URL, no need to modify
            return next_page
        elif next_page.startswith('/'):
            # Relative URL, join with current page's URL
            return urljoin(current_page_url, next_page)
        else:
            # Handle other cases, or ignore if needed
            return None

    def is_google_images_link(self, url):
        parsed_url = urlparse(url)
        #print("FULL URL: " + url)
        #print("COUNT: " + self.count("https"))
        return url.count("https") == 1 or "imgres" in url 