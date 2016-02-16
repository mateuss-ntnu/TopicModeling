__author__ = 'Mateusz'

import re
import logging
import nltk
import sys
from multiprocessing.managers import BaseManager

class MyManager(BaseManager): pass

def Manager():
    m = MyManager()
    m.start()
    return m

class BowCorpus(object):
  def __init__(self):
    self._corpus = None

  def set_corpus(self, value):
    self._corpus = value

  def get_corpus(self):
      return self._corpus

class TfidfCorpus(object):
  def __init__(self):
    self._corpus = None

  def set_corpus(self, value):
    self._corpus = value

  def get_corpus(self):
      return self._corpus



def gen_tfidf(corpus):
    print "Started tfidf"
    tStart = time()
    tfidf = models.TfidfModel(corpus, normalize=True)
    tStop = time()
    print "Running time tfidf: %f" % (tStop - tStart)
    pathtfidf = pathModelFolder + '/model.tfidf'
    tfidf.save(pathtfidf)
    return tfidf


def gen_lsi(corpus,topics,comment):
    print "Started lsi "+comment+" "+str(topics)
    tStart = time()
    lsi = models.LsiModel(corpus.get_corpus(), id2word=dictionary, num_topics=topics)
    tStop = time()
    print "Running time lsi "+comment+str(topics)+": %f" % (tStop - tStart)
    #lsi.save('/Volumes/My Passport/gensim-wiki-ensimple/models/model.lsi')
    pathlsi = pathModelFolder + '/model-'+comment+'-'+str(topics)+'.lsi'
    lsi.save(pathlsi)

def gen_lda(corpus,topics,comment):
    print "Started lda"+comment+" "+str(topics)
    tStart = time()
    lda = models.LdaModel(corpus=corpus.get_corpus(), id2word=dictionary, update_every=1, num_topics=topics)
    tStop = time()
    print "Running time lda "+comment+str(topics)+": %f" % (tStop - tStart)
    pathlda = pathModelFolder + '/model-'+comment+'-'+str(topics)+'.lda'
    lda.save(pathlda)

def gen_ldaMultiCore(corpus,topics,comment):
    print "Started lda multicore"+comment+" "+str(topics)
    tStart = time()
    import multiprocessing as mp
    lda = models.LdaMulticore(corpus=corpus.get_corpus(), id2word =dictionary, workers=(mp.cpu_count()/2-1), num_topics=topics)
    tStop = time()
    print "Running time lda multicore "+comment+str(topics)+": %f" % (tStop - tStart)
    pathldamulti = pathModelFolder + '/model-'+comment+'-'+str(topics)+'.ldamulti'
    lda.save(pathldamulti)

def gen_rp(corpus, topics, comment):
    print "Started rp "+comment+" "+str(topics)
    tStart = time()
    rp = models.RpModel(corpus.get_corpus(), num_topics=topics, id2word=dictionary)
    tStop = time()
    print "Running time rp "+comment+str(topics)+": %f" % (tStop - tStart)
    #rp.save('/Volumes/My Passport/gensim-wiki-ensimple/models/model.rp')
    pathrp = pathModelFolder + '/model-'+comment+'-'+str(topics)+'.rp'
    rp.save(pathrp)


def gen_hdp(corpus,comment):
    print "Started hdp"+comment
    tStart = time()
    hdp = models.HdpModel(corpus.get_corpus(), id2word=dictionary)
    tStop = time()
    print "Running time hdp "+comment+": %f" % (tStop - tStart)
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

MyManager.register('BowCorpus', BowCorpus)
MyManager.register('TfidfCorpus', TfidfCorpus)


import multiprocessing as mp

    #for hypethreaded procs
    #pool =  mp.Pool(processes=(mp.cpu_count()/2-1))
if __name__ == '__main__':
    pool = mp.Pool(processes=3)

    manager = Manager()
    bow_c = manager.BowCorpus()
    tfidf_c = manager.TfidfCorpus()

    bow_c.set_corpus(corpus)
    tfidf_c.set_corpus(corpus_tfidf)

    num_topics = [10, 20, 50, 100, 200]#

    comment = "tfidf"
    pool.apply_async(gen_lda, (tfidf_c, 200, comment))
    comment = "bow"
    pool.apply_async(gen_rp, (bow_c, 500, comment))
    pool.apply_async(gen_lda, (bow_c, 500, comment))
    pool.apply_async(gen_lsi, (bow_c, 500, comment))

    pool.close()
    pool.join()






