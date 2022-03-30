import os
import json
import sys
from scrapy.selector import Selector

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config.config import CORPUS_DIR, CORPUS_METADATA

BODY_NODES = ['//p//text()', '//ul//text()', '//h2//text()', '//h1//text()',
              '//h3//text()', '//h4//text()', '//h5//text()']


class Parser:

    def parse(self, filename):
        print(f"\nparser: parsing {filename}.")
        try:
            file = open(filename)
            selector = Selector(text=file.read())
            title = selector.xpath('//title//text()').get()
            body = ''.join(selector.xpath('|'.join(BODY_NODES)).getall())
            summary = ''.join(selector.xpath('//p//text()').getall()).split('.')[0] + "."
            file.close()
            return title, body, summary
        except FileNotFoundError as e:
            print(e)
            return None, None

    def write_doc(self, filename, text):
        print(f"parser: write document to {filename}")
        try:
            with open(filename, "w") as f:
                f.write(text)
                f.close()
            print(f"parser: successfully updated write document {filename}.")
        except Exception:
            print(f"[error] parser: cannot write document {filename}.")

    def write_metadata(self, metadata):
        print(f"\nparser: update corpus metadata {CORPUS_METADATA}.")
        try:
            with open(CORPUS_METADATA, "w") as f:
                json.dump(metadata, f, indent=4)
                f.close()
            print("parser: successfully updated corpus metadata.")
        except Exception:
            print("[error] parser: cannot update corpus metadata.")

    def run(self):
        corpus_metadata = []

        if not os.path.isfile(CORPUS_METADATA):
            print("\nparser: cannot find corpus metadata file.")
            exit(1)

        try:
            with open(CORPUS_METADATA, "r") as f:
                documents = json.load(f)
                for document in documents:
                    htmlfile = document['htmlfile']

                    if not os.path.isfile(htmlfile):
                        print(f"\nparser: cannot find {htmlfile}")
                        continue

                    filename = document["name"] + ".txt"
                    filedir = os.path.join(CORPUS_DIR, filename)

                    title, body, summary = self.parse(htmlfile)

                    if title and body:
                        text = f"{title}\n{body}"
                        self.write_doc(filedir, text)

                        document['title'] = title
                        document['summary'] = summary
                        document['docfile'] = filedir
                        corpus_metadata.append(document)
                    else:
                        print(f"parser: cannot parse {htmlfile}.")

                f.close()

            self.write_metadata(corpus_metadata)

        except Exception:
            print("parser: cannot read corpus metadata.")


if __name__ == "__main__":
    parser = Parser()
    parser.run()
