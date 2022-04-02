from scrapy.crawler import CrawlerProcess
from crawler import WikiSpider
from parser import Parser

if __name__ == "__main__":
    # start crawler process
    process = CrawlerProcess()
    process.crawl(WikiSpider)
    process.start()

    # start parser
    parser = Parser()
    parser.run()
