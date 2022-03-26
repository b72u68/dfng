import os
import json
from scrapy.selector import Selector

BODY_NODES = ['//p//text()', '//ul//text()', '//h2//text()', '//h1//text()',
              '//h3//text()', '//h4//text()', '//h5//text()']

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.join(ROOT_DIR, "data")
CORPUS_METADATA = os.path.join(DATA_DIR, "corpus.json")
CORPUS_DIR = os.path.join(DATA_DIR, "docs")


def parse(filename):
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


def write(filename, text):
    with open(filename, "w") as f:
        f.write(text)
        f.close()


if __name__ == "__main__":

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
            title, body = parse(htmlfile)

            if title and body:
                text = f"{title}\n{body}"
                print(f"parser: write document {filedir}")
                write(filedir, text)

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
