__author__ = 'Mateusz'

import re
import logging
import nltk
import sys


def gen_tfidf(corpus):
    print "Started tfidf"
    tStart = time()
    tfidf = models.TfidfModel(corpus, normalize=True)
    tStop = time()
    print "Running time tfidf: %f" % (tStop - tStart)
    #tfidf.save('/Volumes/My Passport/gensim-wiki-ensimple/models/model.tfidf')
    pathtfidf = pathModelFolder + '/model.tfidf'
    #tfidf.save(pathtfidf)
    return tfidf


def gen_lsi(corpus,topics,comment):
    print "Started lsi "+comment+" "+str(topics)
    tStart = time()
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=topics)
    tStop = time()
    print "Running time lsi: %f" % (tStop - tStart)
    #lsi.save('/Volumes/My Passport/gensim-wiki-ensimple/models/model.lsi')
    pathlsi = pathModelFolder + '/model-'+comment+str(topics)+'-.lsi'
    lsi.save(pathlsi)

def gen_lda(corpus,topics,comment):
    print "Started lda"+comment+" "+str(topics)
    tStart = time()
    lda = models.LdaModel(corpus=corpus, id2word=dictionary, update_every=1, num_topics=topics)
    tStop = time()
    print "Running time lda: %f" % (tStop - tStart)
    pathlda = pathModelFolder + '/model-'+comment+str(topics)+'-.lda'
    lda.save(pathlda)

def gen_ldaMultiCore(corpus,topics,comment):
    print "Started lda multicore"+comment+" "+str(topics)
    tStart = time()
    import multiprocessing as mp
    lda = models.LdaMulticore(corpus=corpus, id2word =dictionary, workers=(mp.cpu_count()/2-1), num_topics=topics)
    tStop = time()
    print "Running time lda multicore: %f" % (tStop - tStart)
    pathldamulti = pathModelFolder + '/model-'+comment+str(topics)+'-.ldamulti'
    lda.save(pathldamulti)

def gen_rp(corpus, topics, comment):
    print "Started rp"+comment+" "+str(topics)
    tStart = time()
    rp = models.RpModel(corpus, num_topics=500, id2word=dictionary)
    tStop = time()
    print "Running time rp: %f" % (tStop - tStart)
    #rp.save('/Volumes/My Passport/gensim-wiki-ensimple/models/model.rp')
    pathrp = pathModelFolder + '/model-'+comment+str(topics)+'-.rp'
    rp.save(pathrp)


def gen_hdp(corpus,comment):
    print "Started hdp"+comment
    tStart = time()
    hdp = models.HdpModel(corpus, id2word=dictionary)
    tStop = time()
    print "Running time rp: %f" % (tStop - tStart)
    #hdp.save('/Volumes/My Passport/gensim-wiki-ensimple/models/model.hdp')
    pathhdp = pathModelFolder + '/model-'+comment+'.hdp'
    hdp.save(pathhdp)

#pathDictionary = '/Volumes/My Passport/gensim-wiki-ensimple/dictionary.dict'
#pathCorpus = '/Volumes/My Passport/gensim-wiki-ensimple/corpus.mm'

if sys.argv.__len__() == 2:
    if (sys.argv[1] is not None):
        pathDictionary = sys.argv[1] + "/dictionary.dict"

    if (sys.argv[1] is not None):
        pathCorpus = sys.argv[1] + "/corpus.mm"
    if (sys.argv[1] is not None):
        pathModelFolder = sys.argv[1] +"/models"

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities

print ('%s/model.rp') %(pathModelFolder)

dictionary = corpora.Dictionary.load(pathDictionary)
corpus = corpora.MmCorpus(pathCorpus)
print(corpus)

new_doc = "Human computer interaction"
new_vec = dictionary.doc2bow(new_doc.lower().split())
print(new_vec)


from time import time

#tfidf = gen_tfidf(corpus)
tfidf = models.TfidfModel.load(pathModelFolder+"/model.tfidf")
corpus_tfidf = tfidf[corpus]

#gen_hdp(corpus_tfidf,"bow")
#gen_hdp(corpus,"tfidf")

num_topics = [10, 20, 50, 100, 200, 500]

comment = "tfidf"
for n in num_topics:
    gen_lsi(corpus_tfidf, n, comment)
    gen_lda(corpus_tfidf, n, comment)
    #gen_ldaMultiCore(corpus_tfidf, n, comment)
    gen_rp(corpus_tfidf,n, comment)

comment = "bow"
for n in num_topics:
    gen_lsi(corpus, n, comment)
    gen_lda(corpus, n, comment)
    #gen_ldaMultiCore(corpus, n, comment)
    gen_rp(corpus,n, comment)








