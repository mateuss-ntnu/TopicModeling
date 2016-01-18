# coding=utf-8
__author__ = 'Mateusz'

import logging
import nltk

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities

# documents = ["Human machine interface for lab abc computer applications",
#              "A survey of user opinion of computer system response time",
#              "The EPS user interface management system",
#              "System and human system engineering testing of EPS",
#              "Relation of user perceived response time to error measurement",
#              "The generation of random binary unordered trees",
#              "The intersection graph of paths in trees",
#              "Graph minors IV Widths of trees and well quasi ordering",
#              "Graph minors A survey"]
documents = [u"""First phase of the Tethys Ocean's forming: the (first) Tethys Sea starts dividing Pangaea into two supercontinents, Laurasia and Gondwana.
The Tethys Ocean existed between the continents of Gondwana and Laurasia during much of the Mesozoic era.
Several smaller versions have existed down to the present day. Today's Black Sea, Caspian Sea, and Aral Sea are remnants of the Tethys.

Names
This is a list of names which have been used for different stages of the Tethys:

Proto-Tethys, from the latest Ediacaran to the Carboniferous 550–330 million years ago (mya)
Palaeo-Tethys or Paleo-Tethys, from Carboniferous to early Jurassic
Tethys Ocean proper, or Neo-Tethys,  existed between the continents of Gondwana and Laurasia before the opening of the Indian and Atlantic oceans during the Cretaceous period. Roughly, a bigger Mediterranean, continuing right through to the Indian Ocean.
Alpine or Paratethys sea to the north of the Tethys, roughly where the Alps are today. """]

# remove common words and tokenize
#stoplist = set('for a of the and to in'.split())
stoplist = set(nltk.corpus.stopwords.words("english"))
texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in documents]

# remove words that appear only once
from collections import defaultdict
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1]
         for text in texts]

from pprint import pprint   # pretty-printer
pprint(texts)

dictionary = corpora.Dictionary(texts)
#dictionary.save('/Users/Mateusz/Desktop/deerwester.dict')
print(dictionary.token2id)

corpus = [dictionary.doc2bow(text) for text in texts]
#corpora.MmCorpus.serialize('/tmp/deerwester.mm', corpus) # store to disk, for later use
pprint(corpus)