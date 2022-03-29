import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
CORPUS_METADATA = os.path.join(DATA_DIR, "corpus.json")
INDEX_DIR = os.path.join(ROOT_DIR, "index")
INDEXFILE = os.path.join(INDEX_DIR, "index.pickle")
