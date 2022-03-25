import os
from scrapy.selector import Selector

TITLE_NODES = ['//h1//text()']
BODY_NODES = ['//p//text()', '//ul//text()', '//h2//text()', '//h3//text()',
              '//h4//text()', '//h5//text()']

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
HTML_DIR = os.path.join(CURRENT_DIR, "html")
DOC_DIR = os.path.join(CURRENT_DIR, "docs")

if not os.path.isdir(DOC_DIR):
    print(f"\nparser: creating docs directory {DOC_DIR}.")
    os.mkdir(DOC_DIR)


def parse(filename):
    try:
        file = open(filename)
        selector = Selector(text=file.read())
        title = selector.xpath('|'.join(TITLE_NODES)).get()
        body = ' '.join(selector.xpath('|'.join(BODY_NODES)).getall())
        file.close()
        return title, body
    except FileNotFoundError as e:
        print(e)
        return None, None


def write_doc(filename, text):
    docfile = os.path.join(DOC_DIR, filename)
    with open(docfile, 'w') as f:
        f.write(text)
        f.close()


if __name__ == "__main__":
    for file in os.listdir(HTML_DIR):
        htmlfile = os.path.join(HTML_DIR, file)

        if not os.path.isfile(htmlfile):
            continue

        docfile = '.'.join(file.split(".")[:-1]) + ".txt"

        print(f"\nparser: parsing {htmlfile}.")
        title, body = parse(htmlfile)

        if title and body:
            text = f'{title}\n\n{body}'
            print(f"parser: writing document {docfile}.")
            write_doc(docfile, text)
        else:
            print(f"parser: cannot parse {htmlfile}.")
