from collections import Counter
from collections import defaultdict
import re
import unicodedata


class LanguageModel(object):

    def tokenize(self, document):
        """ convert document into list of tokens. """
        document = unicodedata.normalize('NFKD', document) \
                              .encode('ascii', 'ignore').decode()
        document = document.lower()
        document = re.sub(r"\[(\d+|\w)\]", "", document)
        document = re.sub(r"[^a-zA-Z0-9 ]", " ", document)
        document = re.sub(r"\s+", " ", document)
        return document.split(" ")

    def doc_to_model(self, document, vocab, smooth=1):
        """ convert document d into language model M_d. """
        counts = Counter(document)
        for term in vocab:
            if term not in counts:
                counts[term] = 0
            counts[term] += smooth
            counts[term] /= (1. * len(document) + smooth * len(vocab))
        return counts

    def p_given_q_m(self, q, m_d):
        p = 1.
        q = self.tokenize(q)
        for qi in q:
            p *= m_d[qi]
        return p

    def docs_to_model(self, documents):
        """ convert corpus into list of language model M_d. """
        mds = []
        vocab = set()

        for i in range(len(documents)):
            documents[i] = self.tokenize(documents[i])
            vocab.update(documents[i])

        for i, doc in enumerate(documents):
            md = self.doc_to_model(doc, vocab)
            mds.append(md)

        return mds

    def ranking(self, q, mds):
        """ ranking documents based on given query q and language models. """
        probs = defaultdict(float)
        for i, md in enumerate(mds):
            probs[i] = self.p_given_q_m(q, md)
        ranks = sorted(probs, key=lambda i: probs[i], reverse=True)
        return [(i, probs[i]) for i in ranks]


documents = ["click go the shears boys click click click", "click click",
             "metal here", "metal shears click here"]

lm = LanguageModel()
model = lm.docs_to_model(documents)
print("click: ", lm.ranking("click", model))
print("shears: ", lm.ranking("shears", model))
print("click shears: ", lm.ranking("click shears", model))
