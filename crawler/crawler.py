import os
import re
import sys
import json
from scrapy import Request
from scrapy import Spider

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config.config import MAX_PAGES, MAX_DEPTH, SEED_URLS, ALLOWED_URLS
from config.config import HTML_DIR, CORPUS_METADATA


class WikiSpider(Spider):

    name = "wikispider"
    allowed_domains = ALLOWED_URLS
    start_urls = SEED_URLS
    custom_settings = {
            # settings AutoThrottle
            # 'AUTOTHROTTLE_ENABLED': True,
            # 'AUTOTHROTTLE_TARGET_CONCURRENCY': 2,

            # maximum pagecounts and depth limit
            'CLOSESPIDER_PAGECOUNT': MAX_PAGES,
            'DEPTH_LIMIT': MAX_DEPTH,

            # settings for FIFO crawling
            'DEPTH_PRIORITY': 1,
            'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
            'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',

            # hide logs, only show errors
            'LOG_ENABLE': False,
            'LOG_LEVEL': 'ERROR'
    }
    visited_urls = set()
    corpus_metadata = []

    def __init__(self, verbose=True, *args, **kwargs):
        super(WikiSpider, self).__init__(*args, **kwargs)
        self.verbose = verbose

    def write_json(self):
        if self.verbose:
            print(f"crawler: write corpus metadata {CORPUS_METADATA}.")
        try:
            with open(CORPUS_METADATA, "w") as f:
                json.dump(self.corpus_metadata, f, indent=4)
                f.close()
            if self.verbose:
                print("crawler: successfully write corpus metadata.")
        except Exception as e:
            print("[error] crawler: cannot write corpus metadata.")
            print(e)
            exit(1)

    def process_filename(self, filename):
        return re.sub(r'[#%&{}\<>*?/$!\'":@+`|= ]', '', filename)

    def parse(self, response):
        depth = response.meta["depth"] if "depth" in response.meta else 0
        parent = response.meta["parent"] if "parent" in response.meta else ""

        if response.status != 404:
            if len(self.visited_urls) >= MAX_PAGES:
                return

            url = response.url
            title = response.xpath('//title//text()').get()
            filename = self.process_filename(title) + ".html"
            filedir = os.path.join(HTML_DIR, filename)

            if self.verbose:
                print(f"crawler: writing html file {filedir}.")
            with open(filedir, 'wb') as f:
                f.write(response.body)
                f.close()

            self.visited_urls.add(url)
            self.corpus_metadata.append({"parent": parent, "depth": depth,
                                         "url": url, "htmlfile": filedir,
                                         "docfile": "", "title": title,
                                         "summary": ""})
            self.write_json()

            for next_page in response.xpath('//p//a/@href').re('/wiki/.+'):
                next_url = response.urljoin(next_page)
                if next_url not in self.visited_urls:
                    request = Request(next_url, callback=self.parse)
                    request.meta["parent"] = url
                    request.meta["depth"] = depth + 1
                    yield request
