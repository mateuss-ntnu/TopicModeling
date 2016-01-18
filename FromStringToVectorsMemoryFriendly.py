__author__ = 'Mateusz'

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities


class MyCorpus(object):
    def __iter__(self):
        for document in open('text.txt'):

            yield dictionary.doc2bow(document.lower().split())


dictionary = corpora.Dictionary(line.lower().split() for line in open('mycorpus.txt'))
# remove stop words and words that appear only once
import nltk
stoplist = set(nltk.corpus.stopwords.words("english"))
stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
dictionary.filter_tokens(stop_ids + once_ids) # remove stop words and words that appear only once
dictionary.compactify()

corpus_memory_friendly = MyCorpus()
print(corpus_memory_friendly)

for vector in corpus_memory_friendly:
    print(vector)

    # # remove common words and tokenize
    # stoplist = set('for a of the and to in'.split())
    # texts = [[word for word in document.lower().split() if word not in stoplist]
    #          for document in documents]
    #
    # # remove words that appear only once
    # from collections import defaultdict
    # frequency = defaultdict(int)
    # for text in texts:
    #     for token in text:
    #         frequency[token] += 1
    #
    # texts = [[token for token in text if frequency[token] > 1]
    #          for text in texts]
    #
    # from pprint import pprint   # pretty-printer
    # pprint(texts)
    #
    # dictionary = corpora.Dictionary(texts)
    # #dictionary.save('/Users/Mateusz/Desktop/deerwester.dict')
    # print(dictionary.token2id)
