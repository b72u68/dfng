import os
import re
import sys
import pickle
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config.config import INDEXFILE

sw = stopwords.words('english')
ps = PorterStemmer()


class Indexer(object):

    def __init__(self, indexfile=INDEXFILE):
        self.INDEXFILE = indexfile
        self.TFIDF_VECTORIZER = TfidfVectorizer(input="content",
                                                strip_accents='ascii',
                                                tokenizer=self.tokenize)

    def tokenize(self, document):
        document = re.sub(r'[^a-zA-Z0-9 ]', ' ', document)
        tokens = word_tokenize(document)
        return [ps.stem(token) for token in tokens if token not in sw]

    def construct_inverted_index(self, documents):
        documents = sorted(documents, key=lambda d: d['title'])
        corpus = [open(document['docfile']).read() for document in documents]
        tfidf_vector = self.TFIDF_VECTORIZER.fit_transform(corpus)
        tfidf_vector.raw_documents = documents
        self.INVERTED_INDEX = tfidf_vector
        return tfidf_vector

    def construct_query_vector(self, query):
        return self.TFIDF_VECTORIZER.transform([query])

    def calculate_cosine_similarity(self, index, query_vector):
        return cosine_similarity(index, query_vector)

    def search(self, index, query, top_k=10):
        raw_documents = index.raw_documents
        query_vector = self.construct_query_vector(query)
        cos_sim_vector = self.calculate_cosine_similarity(index, query_vector)
        sorted_result = sorted(enumerate(raw_documents),
                               key=lambda x: cos_sim_vector[x[0]],
                               reverse=True)
        return [(cos_sim_vector[doc[0]], doc[1])
                for doc in sorted_result[:top_k]]

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
