__author__ = 'Mateusz'

import re
import logging
import nltk
import sys


def gen_tfidf():
    print "Started tfidf"
    tStart = time()
    tfidf = models.TfidfModel(bow_corpus, normalize=True)
    tStop = time()
    print "Running time tfidf: %f" % (tStop - tStart)
    #tfidf.save('/Volumes/My Passport/gensim-wiki-ensimple/models/model.tfidf')
    pathtfidf = pathModelFolder + '/model.tfidf'
    tfidf.save(pathtfidf)

    #thread.start_new_thread(gen_lsi())
    #thread.start_new_thread(gen_hdp())
    # thread_lsi = Process(target=gen_lsi())
    # thread_lsi.start()
    # thread_lsi.join()
    # thread_rp = Process(target=gen_rp())
    # thread_rp.start()
    # thread_rp.join()


def gen_lsi():
    print "Started lsi"
    tStart = time()
    lsi = models.LsiModel(tfidf, id2word=dictionary, num_topics=300)
    tStop = time()
    print "Running time lsi: %f" % (tStop - tStart)
    #lsi.save('/Volumes/My Passport/gensim-wiki-ensimple/models/model.lsi')
    pathlsi = pathModelFolder + '/model.lsi'
    lsi.save(pathlsi)


def gen_rp():
    print "Started rp"
    tStart = time()
    rp = models.RpModel(tfidf, num_topics=500)
    tStop = time()
    print "Running time rp: %f" % (tStop - tStart)
    #rp.save('/Volumes/My Passport/gensim-wiki-ensimple/models/model.rp')
    pathrp = pathModelFolder + '/model.rp'
    rp.save(pathrp)


def gen_hdp():
    print "Started hdp"
    tStart = time()
    hdp = models.HdpModel(bow_corpus, id2word=dictionary)
    tStop = time()
    print "Running time rp: %f" % (tStop - tStart)
    #hdp.save('/Volumes/My Passport/gensim-wiki-ensimple/models/model.hdp')
    pathhdp = pathModelFolder + '/model.hdp'
    hdp.save(pathhdp)

#pathDictionary = '/Volumes/My Passport/gensim-wiki-ensimple/dictionary.dict'
#pathCorpus = '/Volumes/My Passport/gensim-wiki-ensimple/corpus.mm'

if sys.argv.__len__() == 4:
    if (sys.argv[1] is not None):
        pathDictionary = sys.argv[1]

    if (sys.argv[2] is not None):
        pathCorpus = sys.argv[2]
    if (sys.argv[3] is not None):
        pathModelFolder = sys.argv[3]

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities

print ('%s/model.rp') %(pathModelFolder)

dictionary = corpora.Dictionary.load(pathDictionary)
bow_corpus = corpora.MmCorpus(pathCorpus)
print(bow_corpus)

new_doc = "Human computer interaction"
new_vec = dictionary.doc2bow(new_doc.lower().split())
print(new_vec)


from time import time

tfidf = None
gen_tfidf()
gen_lsi()
gen_rp()







