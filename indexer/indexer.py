import os
import re
import json
import pandas as pd
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt')
nltk.download('stopwords')

sw = stopwords.words('english')
ps = PorterStemmer()

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.join(ROOT_DIR, "data")
CORPUS_METADATA = os.path.join(DATA_DIR, "corpus.json")


def tokenize(document):
    document = re.sub(r'[^a-zA-Z ]', ' ', document)
    tokens = word_tokenize(document)
    return [ps.stem(token) for token in tokens if token not in sw]


def construct_inverted_index(documents):
    tfidf_vectorizer = TfidfVectorizer(input="content", strip_accents='ascii',
                                       tokenizer=tokenize)
    corpus = [open(document['docfile']).read() for document in documents]
    index = [document['name'] for document in documents]
    tfidf_vector = tfidf_vectorizer.fit_transform(corpus)
    tfidf_df = pd.DataFrame(tfidf_vector.toarray(), index=index,
                            columns=tfidf_vectorizer.get_feature_names_out())
    return tfidf_df


if __name__ == "__main__":
    corpus_metadata = []
    with open(CORPUS_METADATA, "r") as f:
        corpus_metadata = json.load(f)

    construct_inverted_index(corpus_metadata)
