import os
import re
import json
import pickle
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import INDEX_DIR, CORPUS_METADATA

sw = stopwords.words('english')
ps = PorterStemmer()


class Indexer:

    def __init__(self, documents=[]):
        self.INDEXFILE = os.path.join(INDEX_DIR, "index.pickle")
        self.TFIDF_VECTORIZER = TfidfVectorizer(input="content",
                                                strip_accents='ascii',
                                                tokenizer=self.tokenize)

    def tokenize(self, document):
        document = re.sub(r'[^a-zA-Z ]', ' ', document)
        tokens = word_tokenize(document)
        return [ps.stem(token) for token in tokens if token not in sw]

    def construct_inverted_index(self, documents):
        documents = sorted(documents, key=lambda d: d["name"])
        corpus = [open(document['docfile']).read() for document in documents]
        index = [document['name'] for document in documents]
        tfidf_vector = self.TFIDF_VECTORIZER.fit_transform(corpus)
        tfidf_vector.target_names = index
        return tfidf_vector

    def construct_query_vector(self, query):
        return self.TFIDF_VECTORIZER.transform([query])

    def calculate_cosine_similarity(self, index, query_vector):
        return cosine_similarity(index, query_vector)

    def write_index(self, index):
        try:
            with open(self.INDEXFILE, 'wb') as f:
                pickle.dump(index, f, pickle.HIGHEST_PROTOCOL)
                f.close()
            return 0
        except Exception:
            return 1

    def load_index(self):
        try:
            with open(self.INDEXFILE, 'rb') as f:
                index = pickle.load(f)
                f.close()
            return index
        except Exception:
            return None


if __name__ == "__main__":
    corpus_metadata = []

    with open(CORPUS_METADATA, "r") as f:
        corpus_metadata = json.load(f)

    indexer = Indexer()

    print("indexer: construct inverted index.")
    index = indexer.construct_inverted_index(corpus_metadata)

    print("indexer: write index to disk.")
    indexer.write_index(index)
