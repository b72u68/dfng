import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
TEST_DIR = os.path.join(ROOT_DIR, "test")
INDEX_DIR = os.path.join(ROOT_DIR, "index")
HTML_DIR = "html"
CORPUS_DIR = "docs"
CORPUS_METADATA = "corpus.json"

URL = "https://en.wikipedia.org/wiki/Compiler"
BASE_URL = "en.wikipedia.org"
MAX_PAGES = 5
MAX_DEPTH = 1
