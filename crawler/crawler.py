import os
import json
from scrapy.crawler import CrawlerProcess
from scrapy import Request
from scrapy import Spider
from config import CrawlerConfig

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.join(ROOT_DIR, "data")
HTML_DIR = os.path.join(DATA_DIR, "html")
CORPUS_METADATA = os.path.join(DATA_DIR, "corpus.json")

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
            'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
            'LOG_ENABLE': False,
            'LOG_LEVEL': 'ERROR'
    }
    visited_urls = set()
    corpus_metadata = []

    def write_json(self):
        print("\ncrawler: write corpus metadata.")
        with open(CORPUS_METADATA, "w") as f:
            json.dump(self.corpus_metadata, f, indent=4)
            f.close()

    def parse(self, response):
        parent = response.meta["parent"] if "parent" in response.meta else ""

        if response.status != 404:
            if len(self.visited_urls) >= CrawlerConfig.MAX_PAGES:
                self.write_json()
                return

            url = response.url
            filename = url.split("/")[-1]
            filedir = os.path.join(HTML_DIR, filename + ".html")

            print(f"\ncrawler: writing html file {filedir}.")
            with open(filedir, 'wb') as f:
                f.write(response.body)
                f.close()

            self.visited_urls.add(url)
            self.corpus_metadata.append({"parent": parent, "name": filename,
                                         "htmlfile": filedir, "url": url})

            for next_page in response.xpath('//p//a/@href').re('/wiki/.+'):
                next_url = response.urljoin(next_page)
                if next_url not in self.visited_urls:
                    request = Request(next_url, callback=self.parse)
                    request.meta["parent"] = url
                    yield request


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(WikiSpider)
    process.start()
    print()
