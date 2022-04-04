import os
import sys
import nltk

indexer_module = os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "indexer"
)
sys.path.append(indexer_module)
from indexer import Indexer


class Processor:

    def __init__(self, indexer):
        self.INDEXER = Indexer().load_index()

    def preprocess_query(self, query):
        tokens = self.INDEXER.tokenize(query)
        return ' '.join(tokens)

    def spelling_correction(self, query):
        terms = query.split(' ')
        index_terms = self.INDEXER.TFIDF_VECTORIZER.get_feature_names_out()
        is_corrected = False
        for i in range(len(terms)):
            q = terms[i]
            if q not in index_terms:
                is_corrected = True
                eds = [(t, nltk.edit_distance(q, t)) for t in index_terms]
                terms[i] = min(eds, key=lambda ed: ed[1])[0]
        return ' '.join(terms) if is_corrected else ''

    def search(self, query, top_k=10):
        index = self.INDEXER.INVERTED_INDEX
        return self.INDEXER.search(index, query, top_k)
