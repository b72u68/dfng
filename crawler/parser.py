import os
import json
from scrapy.selector import Selector
from config import CORPUS_DIR, CORPUS_METADATA

BODY_NODES = ['//p//text()', '//ul//text()', '//h2//text()', '//h1//text()',
              '//h3//text()', '//h4//text()', '//h5//text()']


class Parser:

    def parse(self, filename):
        try:
            file = open(filename)
            selector = Selector(text=file.read())
            title = selector.xpath('//title//text()').get()
            body = ' '.join(selector.xpath('|'.join(BODY_NODES)).getall())
            file.close()
            return title, body
        except FileNotFoundError as e:
            print(e)
            return None, None

    def write_doc(self, filename, text):
        with open(filename, "w") as f:
            f.write(text)
            f.close()

    def run(self):
        corpus_metadata = []

        if not os.path.isfile(CORPUS_METADATA):
            print("\nparser: cannot find corpus metadata file.")
            exit(1)

        with open(CORPUS_METADATA, "r") as f:
            documents = json.load(f)
            for document in documents:
                htmlfile = document['htmlfile']

                if not os.path.isfile(htmlfile):
                    print(f"\nparser: cannot find {htmlfile}")
                    continue

                filename = document["name"] + ".txt"
                filedir = os.path.join(CORPUS_DIR, filename)

                print(f"\nparser: parsing {htmlfile}.")
                title, body = self.parse(htmlfile)

                if title and body:
                    text = f"{title}\n{body}"
                    print(f"parser: write document to {filedir}")
                    self.write_doc(filedir, text)

                    document['title'] = title
                    document['docfile'] = filedir
                    corpus_metadata.append(document)
                else:
                    print(f"parser: cannot parse {htmlfile}.")

            f.close()

        print("\nparser: update corpus metadata.")
        with open(CORPUS_METADATA, "w") as f:
            json.dump(corpus_metadata, f, indent=4)
            f.close()


if __name__ == "__main__":
    parser = Parser()
    parser.run()
