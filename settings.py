import nltk
import os
from config.config import DATA_DIR, HTML_DIR, CORPUS_DIR, INDEX_DIR

if not os.path.isdir(DATA_DIR):
    print(f"settings: creating data directory {DATA_DIR}.")
    os.mkdir(DATA_DIR)

if not os.path.isdir(HTML_DIR):
    print(f"settings: creating data/html directory {HTML_DIR}.")
    os.mkdir(HTML_DIR)

if not os.path.isdir(CORPUS_DIR):
    print(f"settings: creating data/docs directory {CORPUS_DIR}.")
    os.mkdir(CORPUS_DIR)

if not os.path.isdir(INDEX_DIR):
    print(f"settings: creating index directory {INDEX_DIR}.")
    os.mkdir(INDEX_DIR)

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    print("settings: installing nltk punkt")
    nltk.download('punkt')

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    print("settings: installing nltk stopwords")
    nltk.download('stopwords')
