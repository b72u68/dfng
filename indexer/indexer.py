import os
import re
import sys
import pickle
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config.config import INDEXFILE

SW = stopwords.words('english')


class Indexer(object):

    def __init__(self, documents=[], indexfile=INDEXFILE):
        self.INDEXFILE = indexfile
        self.TFIDF_VECTORIZER = TfidfVectorizer(input="content",
                                                strip_accents='ascii',
                                                tokenizer=self.tokenize)
        if len(documents):
            self.documents = sorted(documents, key=lambda d: d['title'])
            self.INVERTED_INDEX = self.construct_inverted_index(self.documents)

    def tokenize(self, document):
        document = re.sub(r"\[(\d+|\w)\]", "", document.lower())
        document = re.sub(r"[^a-zA-Z0-9 ]", " ", document)
        tokens = word_tokenize(document)
        return [t for t in tokens if t not in SW]

    def construct_inverted_index(self, documents):
        corpus = [open(d['docfile']).read() for d in documents if d['docfile']]
        tfidf_vector = self.TFIDF_VECTORIZER.fit_transform(corpus)
        return tfidf_vector

    def construct_query_vector(self, query):
        return self.TFIDF_VECTORIZER.transform([query])

    def calculate_cosine_similarity(self, index, query_vector):
        return cosine_similarity(index, query_vector).flatten()

    def search(self, index, query, top_k=10):
        query_vector = self.construct_query_vector(query)
        cos_sim_vector = self.calculate_cosine_similarity(index, query_vector)
        sorted_result = sorted(enumerate(self.documents),
                               key=lambda x: cos_sim_vector[x[0]],
                               reverse=True)
        result = []
        for i, doc in enumerate(sorted_result):
            doc_id = doc[0]
            if i == top_k:
                break
            if cos_sim_vector[doc_id] > 0:
                doc_obj = {"parent": doc[1]["parent"], "url": doc[1]["url"],
                           "title": doc[1]["title"],
                           "summary": doc[1]["summary"]}
                result.append((cos_sim_vector[doc_id], doc_obj))
        return result[:top_k]

    def write_index(self):
        try:
            with open(self.INDEXFILE, 'wb') as f:
                pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
                f.close()
            return 0
        except Exception as e:
            print('[error] indexer: cannot write index to disk.')
            print(e)
            exit(1)

    def load_index(self):
        try:
            with open(self.INDEXFILE, 'rb') as f:
                index = pickle.load(f)
                f.close()
            return index
        except Exception as e:
            print('[error] indexer: cannot load index from disk.')
            print(e)
            exit(1)
