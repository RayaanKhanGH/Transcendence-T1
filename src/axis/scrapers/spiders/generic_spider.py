import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import json
import sys
import os

class UniversalSpider(scrapy.Spider):
    name = "universal_spider"
    
    def __init__(self, urls=None, *args, **kwargs):
        super(UniversalSpider, self).__init__(*args, **kwargs)
        if urls:
            self.start_urls = urls.split(',')
        else:
            self.start_urls = []
            
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url, 
                callback=self.parse,
                errback=self.errback,
                meta={'handle_httpstatus_list': [403, 404, 500, 503]}
            )

    def parse(self, response):
        yield {
            'url': response.url,
            'status': response.status,
            'html': response.text,
            'title': response.css('title::text').get(),
            'error': None
        }

    def errback(self, failure):
        yield {
            'url': failure.request.url,
            'status': 0,
            'html': '',
            'title': None,
            'error': str(failure.value)
        }

def run_spider(urls, output_file):
    settings = get_project_settings()
    settings.set('FEED_FORMAT', 'json')
    settings.set('FEED_URI', output_file)
    settings.set('LOG_LEVEL', 'ERROR')
    settings.set('USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    settings.set('ROBOTSTXT_OBEY', False)
    settings.set('COOKIES_ENABLED', False)
    
    process = CrawlerProcess(settings)
    process.crawl(UniversalSpider, urls=urls)
    process.start()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generic_spider.py <comma_separated_urls> <output_file>")
        sys.exit(1)
        
    urls_arg = sys.argv[1]
    output_file_arg = sys.argv[2]
    
    # Clean up previous output if exists
    if os.path.exists(output_file_arg):
        os.remove(output_file_arg)
        
    run_spider(urls_arg, output_file_arg)
