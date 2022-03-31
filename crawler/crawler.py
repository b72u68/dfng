import os
import sys
import json
from scrapy.crawler import CrawlerProcess
from scrapy import Request
from scrapy import Spider
from crawler_config import MAX_PAGES, MAX_DEPTH, URL, BASE_URL

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config.config import DATA_DIR, HTML_DIR, CORPUS_METADATA


class WikiSpider(Spider):

    name = "wikispider"
    allowed_domains = [BASE_URL]
    start_urls = [URL]
    custom_settings = {
            'CLOSESPIDER_PAGECOUNT': MAX_PAGES,
            'DEPTH_LIMIT': MAX_DEPTH,
            'DEPTH_PRIORITY': 1,
            'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
            'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
            'LOG_ENABLE': False,
            'LOG_LEVEL': 'ERROR'
    }
    visited_urls = set()
    corpus_metadata = []

    def write_json(self):
        print(f"crawler: write corpus metadata {CORPUS_METADATA}.")
        try:
            with open(CORPUS_METADATA, "w") as f:
                json.dump(self.corpus_metadata, f, indent=4)
                f.close()
            print("crawler: successfully write corpus metadata.")
        except Exception as e:
            print("[error] crawler: cannot write corpus metadata.")
            print(e)
            exit(1)

    def parse(self, response):
        parent = response.meta["parent"] if "parent" in response.meta else ""

        if response.status != 404:
            if len(self.visited_urls) >= MAX_PAGES:
                return

            url = response.url
            filename = url.split("/")[-1]
            filedir = os.path.join(HTML_DIR, filename + ".html")

            print(f"crawler: writing html file {filedir}.")
            with open(filedir, 'wb') as f:
                f.write(response.body)
                f.close()

            self.visited_urls.add(url)
            self.corpus_metadata.append({"parent": parent, "url": url,
                                         "htmlfile": filedir, "docfile": ""})
            self.write_json()

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
