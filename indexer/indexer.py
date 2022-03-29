import re
import pickle
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import INDEXFILE

sw = stopwords.words('english')
ps = PorterStemmer()


class Indexer:

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
        documents = sorted(documents, key=lambda d: d['name'])
        corpus = [open(document['docfile']).read() for document in documents]
        tfidf_vector = self.TFIDF_VECTORIZER.fit_transform(corpus)
        tfidf_vector.raw_documents = documents
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
        return sorted_result[:top_k]

    def write_index(self, index):
        try:
            with open(self.INDEXFILE, 'wb') as f:
                pickle.dump(index, f, pickle.HIGHEST_PROTOCOL)
                f.close()
            return 0
        except Exception as e:
            print(e.with_traceback)
            return 1

    def load_index(self):
        try:
            with open(self.INDEXFILE, 'rb') as f:
                index = pickle.load(f)
                f.close()
            return index
        except Exception:
            return None
