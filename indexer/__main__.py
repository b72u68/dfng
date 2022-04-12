import os
import sys
import json
from indexer import Indexer
from time import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config.config import CORPUS_METADATA

if __name__ == "__main__":
    corpus_metadata = []

    try:
        start = time()
        with open(CORPUS_METADATA, "r") as f:
            corpus_metadata = json.load(f)
            f.close()

        if not corpus_metadata:
            print("[error] indexer: cannot load corpus metadata.")
            exit(1)

        indexer = Indexer(documents=corpus_metadata)

        print("indexer: write index to disk.")
        indexer.write_index()
        print("indexer: write index successfully.")
        end = time()
        print("indexer: total indexing time =", end - start, "s")

    except Exception as e:
        print("[error] indexer: cannot load corpus metadata.")
        print(e)
        exit(1)
