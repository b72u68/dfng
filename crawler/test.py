import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config.config import MAX_PAGES, MAX_DEPTH, SEED_URLS
from config.config import HTML_DIR, CORPUS_METADATA

if not os.path.isfile(CORPUS_METADATA):
    print("[test] create corpus metadata: failed")
    print("unable to find corpus metadata file.")
    exit(1)

meta_documents = []
try:
    with open(CORPUS_METADATA, "rb") as f:
        meta_documents = json.load(f)
        f.close()
except Exception as e:
    print("[test] load corpus metadata: failed")
    print(e)
    exit(1)

if not meta_documents:
    print("[test] load corpus metadata: failed")
    exit(1)

if len(meta_documents) > MAX_PAGES:
    print("[test] check number of crawled pages: failed")
    print("number of crawled pages exceeds the number of max pages.")
    exit(1)

max_depth = 0
for doc in meta_documents:
    htmlfile = doc["htmlfile"]
    docfile = doc["docfile"]

    if not os.path.isfile(htmlfile):
        print("[test] check html document: failed")
        print(f"unable to find {htmlfile}.")
        exit(1)

    if not os.path.isfile(docfile):
        print("[test] check text document: failed")
        print(f"unable to find {docfile}.")
        exit(1)

    parent = doc["parent"]
    url = doc["url"]
    if not parent and url not in SEED_URLS:
        print("[test] check seed urls: failed")
        print("unmatch seed urls.")
        exit(1)
    max_depth = max(doc["depth"], max_depth)

if max_depth + 1 > MAX_DEPTH:
    print("[test] check number of depths: failed")
    print("number of depths exceeds the maximum number of depths.")
    exit(1)

print("[test] crawler and parser test: passed")
