from scrapy.crawler import CrawlerProcess
from crawler import WikiSpider
from parser import Parser
from time import time

if __name__ == "__main__":
    # start crawler process
    cstart = time()
    process = CrawlerProcess()
    process.crawl(WikiSpider, verbose=False)
    process.start()
    cend = time()

    # start parser
    pstart = time()
    parser = Parser(verbose=False)
    parser.run()
    pend = time()

    # get total execution time
    print("\ncrawler: total crawling time =", cend - cstart, "s")
    print("parser: total parsing time =", pend - pstart, "s")
