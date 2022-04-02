import os

# directories
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
HTML_DIR = os.path.join(DATA_DIR, "html")
CORPUS_DIR = os.path.join(DATA_DIR, "docs")
CORPUS_METADATA = os.path.join(DATA_DIR, "corpus.json")
INDEX_DIR = os.path.join(ROOT_DIR, "index")
INDEXFILE = os.path.join(INDEX_DIR, "index.pickle")

# config for crawler
SEED_URLS = ["https://en.wikipedia.org/wiki/Compiler"]
ALLOWED_URLS = ["en.wikipedia.org"]
MAX_PAGES = 500
MAX_DEPTH = 10
