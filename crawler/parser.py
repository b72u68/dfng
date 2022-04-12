import os
import json
import re
import sys
from scrapy.selector import Selector

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config.config import CORPUS_DIR, CORPUS_METADATA

NODES = [
    '//p[not(descendant::*[@id="coordinates"]) and not(descendant::style)]//text()',
    '//ul[not(ancestor::footer) and not(ancestor::div[@id="mw-panel" or @id="mw-navigation" or @role="navigation"])]//text()',
    '//h1[not(ancestor::div[@id="mw-panel" or @id="mw-navigation"])]//text()',
    '//h2[not(ancestor::div[@id="mw-panel" or @id="mw-navigation"])]//text()',
    '//h3[not(ancestor::div[@id="mw-panel" or @id="mw-navigation"])]//text()',
    '//h4[not(ancestor::div[@id="mw-panel" or @id="mw-navigation"])]//text()',
    '//h5[not(ancestor::div[@id="mw-panel" or @id="mw-navigation"])]//text()',
]


class Parser:

    def __init__(self, verbose=True):
        self.verbose = verbose

    def parse_summary(self, selector):
        raw_summary = ''.join(selector.xpath(NODES[0]).getall()).split('.')[0]
        summary = re.sub(r'\[(\d+|\w)\]', '', raw_summary.strip("\n")) + "."
        return summary

    def parse(self, filename):
        if self.verbose:
            print(f"\nparser: parsing {filename}.")
        try:
            file = open(filename)
            selector = Selector(text=file.read())
            body = ' '.join(selector.xpath('|'.join(NODES)).getall())
            summary = self.parse_summary(selector)
            file.close()
            return body, summary
        except FileNotFoundError as e:
            print(e)
            return None, None, None

    def write_doc(self, filename, text):
        if self.verbose:
            print(f"parser: write document to {filename}")
        try:
            with open(filename, "w") as f:
                f.write(text)
                f.close()
            if self.verbose:
                print(f"parser: successfully updated document {filename}.")
        except Exception:
            print(f"[error] parser: cannot write document {filename}.")

    def write_metadata(self, metadata):
        if self.verbose:
            print(f"\nparser: update corpus metadata {CORPUS_METADATA}.")
        try:
            with open(CORPUS_METADATA, "w") as f:
                json.dump(metadata, f, indent=4)
                f.close()
            if self.verbose:
                print("parser: successfully updated corpus metadata.")
        except Exception as e:
            print("[error] parser: cannot update corpus metadata.")
            print(e)

    def process_filename(self, filename):
        return re.sub(r'[#%&{}\<>*?/$!\'":@+`|= ]', '', filename)

    def run(self):
        corpus_metadata = []

        if not os.path.isfile(CORPUS_METADATA):
            print("\n[error] parser: cannot find corpus metadata file.")
            exit(1)

        try:
            with open(CORPUS_METADATA, "r") as f:
                documents = json.load(f)
                for document in documents:
                    htmlfile = document['htmlfile']

                    if not os.path.isfile(htmlfile):
                        print(f"\nparser: cannot find {htmlfile}")
                        continue

                    body, summary = self.parse(htmlfile)

                    if body and summary:
                        title = document['title']
                        filename = self.process_filename(title) + ".txt"
                        filedir = os.path.join(CORPUS_DIR, filename)

                        text = f"{title}\n{body}"
                        self.write_doc(filedir, text)

                        document['summary'] = summary
                        document['docfile'] = filedir
                        corpus_metadata.append(document)
                    else:
                        print(f"[error] parser: cannot parse {htmlfile}.")

                f.close()

            self.write_metadata(corpus_metadata)

        except Exception as e:
            print("[error] parser: cannot read corpus metadata.")
            print(e)


if __name__ == "__main__":
    parser = Parser()
    parser.run()
