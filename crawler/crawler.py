import os
from scrapy.crawler import CrawlerProcess
from scrapy import Request
from scrapy import Spider
from config import CrawlerConfig

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
HTML_DIR = os.path.join(CURRENT_DIR, "html")

if not os.path.isdir(HTML_DIR):
    print(f"\ncrawler: creating html directory {HTML_DIR}.")
    os.mkdir(HTML_DIR)


class WikiSpider(Spider):
    name = "wikispider"
    allowed_domains = [CrawlerConfig.BASE_URL]
    start_urls = [CrawlerConfig.URL]
    custom_settings = {
            'CLOSESPIDER_PAGECOUNT': CrawlerConfig.MAX_PAGES,
            'DEPTH_LIMIT': CrawlerConfig.MAX_DEPTH,
            'DEPTH_PRIORITY': 1,
            'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
            'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue'
    }
    visited_urls = set()

    def parse(self, response):
        if response.status != 404:
            if len(self.visited_urls) >= CrawlerConfig.MAX_PAGES:
                return

            url = response.url
            filename = url.split("/")[-1] + ".html"
            filedir = os.path.join(HTML_DIR, filename)

            print(f"crawler: writing html file {filedir}.")
            with open(filedir, 'wb') as f:
                f.write(response.body)
                f.close()

            self.visited_urls.add(url)

            for next_page in response.xpath('//p//a/@href').re('/wiki/.+'):
                url = response.urljoin(next_page)
                if url not in self.visited_urls:
                    yield Request(url, callback=self.parse)


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(WikiSpider)
    process.start()
    print()
