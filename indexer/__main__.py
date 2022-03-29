import json
from indexer import Indexer
from config import CORPUS_METADATA

if __name__ == "__main__":
    corpus_metadata = []

    with open(CORPUS_METADATA, "r") as f:
        corpus_metadata = json.load(f)

    indexer = Indexer()

    print("indexer: construct inverted index.")
    index = indexer.construct_inverted_index(corpus_metadata)

    print("indexer: write index to disk.")
    status = indexer.write_index(index)
    if not status:
        print("indexer: write index successfully.")
    else:
        print("[error] indexer: cannot write index to disk.")
