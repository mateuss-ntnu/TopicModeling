import re
import logging
import nltk
import sys
from gensim import corpora, models, similarities

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

pathTFIDF = '/Volumes/My Passport/gensim-wiki-ensimple/models/model.tfidf'

pathLsi = '/Volumes/My Passport/gensim-wiki-ensimple/models/model.lsi'
pathLsi2 = '/Volumes/My Passport/gensim-wiki-ensimple/models/model2.lsi'
pathLsi3 = '/Volumes/My Passport/gensim-wiki-ensimple/models/model3.lsi'
pathLsi100 = '/Volumes/My Passport/gensim-wiki-ensimple/models/model100.lsi'

pathLsi10_tf = '/Volumes/My Passport/gensim-wiki-ensimple/models/model10_tf.lsi'
pathLsi50_tf = '/Volumes/My Passport/gensim-wiki-ensimple/models/model50_tf.lsi'
pathLsi100_tf = '/Volumes/My Passport/gensim-wiki-ensimple/models/model100_tf.lsi'
pathLsi300_tf = '/Volumes/My Passport/gensim-wiki-ensimple/models/model300_tf.lsi'

pathLda10 = '/Volumes/My Passport/gensim-wiki-ensimple/models/model10.lda'
pathLda10_tf = '/Volumes/My Passport/gensim-wiki-ensimple/models/model10_tf.lda'
pathLda50 = '/Volumes/My Passport/gensim-wiki-ensimple/models/model50.lda'
pathLda50_tf = '/Volumes/My Passport/gensim-wiki-ensimple/models/model50_tf.lda'

pathDictionary = '/Volumes/My Passport/gensim-wiki-ensimple/dictionary.dict'
pathCorpus = '/Volumes/My Passport/gensim-wiki-ensimple/corpus.mm'
pathIndex = '/Volumes/My Passport/gensim-wiki-ensimple/index.index'
query = "Human computer interaction"

createLsi = False
createLda = False
createIndex = False


corpus = corpora.MmCorpus(pathCorpus)
dictionary = corpora.Dictionary.load(pathDictionary)
tfidf = models.TfidfModel.load(pathTFIDF)

#lsi = models.LsiModel.load(pathLsi)

corpus_tfidf = tfidf[corpus]


if(createLsi):
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=100)
    lsi.save(pathLsi100_tf)
else:
    lsi = models.LsiModel.load(pathLsi50_tf)
    #lsi = models.LsiModel.load(pathLsi2)
if(createLda):
    lda = models.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=50, update_every=1, chunksize=10000, passes=1)
    lda.save(pathLda50_tf)
else:
    lda = models.LdaModel.load(pathLda50)

query_bow = dictionary.doc2bow(query.lower().split())
query_lsi = lsi[query_bow]

if(createIndex):
    index = similarities.MatrixSimilarity(lsi[corpus])
    index.save(pathIndex)
else:
    index = similarities.Similarity.load(pathIndex)
print ' '
#topics =lsi.show_topics(num_topics=-1, num_words=-1, log=False, formatted=True)
topics_lsi = lsi.print_topics(-1)
print ' '
topics_lda = lda.print_topics(-1)

# sims = index[query_lsi]
# sims = sorted(enumerate(sims), key=lambda item: -item[1])
#
# print(sims)
