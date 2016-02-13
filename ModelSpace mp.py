__author__ = 'Mateusz'

import re
import logging
import nltk
import sys
from multiprocessing import Process


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


def gen_lsi(corpus,topics):
    print "Started lsi"
    tStart = time()
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=topics)
    tStop = time()
    print "Running time lsi: %f" % (tStop - tStart)
    #lsi.save('/Volumes/My Passport/gensim-wiki-ensimple/models/model.lsi')
    pathlsi = pathModelFolder + '/model.lsi'
    lsi.save(pathlsi)

#def gen_lda(corpus,topics):
#    print "Started lda"
#    tStart = time()
#    #lda = models.LdaModel(corpus=corpus, id2word=dictionary, update_every=0, num_topics=topics)
#    #extract 100 LDA topics, using 1 pass and updating once every 1 chunk (10,000 documents)
#    lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=100, update_every=1, chunksize=10000, passes=1)
#    tStop = time()
#    print "Running time lda: %f" % (tStop - tStart)
#    pathlda = pathModelFolder + '/model-official-gensim.lda'
#    lda.save(pathlda)

def gen_lda(corpus,topics,comment,passes):
    print "Started lda"+comment+" "+str(topics)
    tStart = time()
    #extract 100 LDA topics, using 1 pass and updating once every 1 chunk (10,000 documents)
    #lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=100, update_every=1, chunksize=100000, passes=1)
    # extract 100 LDA topics, using 20 full passes, no online updates
    lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=topics, update_every=0, passes=passes)
    tStop = time()
    print "Running time lda: %f" % (tStop - tStart)
    pathlda = pathModelFolder + '/model-'+comment+'-'+str(topics)+'.lda'
    lda.save(pathlda)

def gen_ldaMultiCore(corpus,topics):
    print "Started lda multicore"
    tStart = time()
    import multiprocessing as mp
    lda = models.LdaMulticore(corpus=corpus, id2word=dictionary, workers=(mp.cpu_count()/2-2), num_topics=topics)
    tStop = time()
    print "Running time lda multicore: %f" % (tStop - tStart)
    pathldamulti = pathModelFolder + '/model.ldamulti'
    lda.save(pathldamulti)

def gen_rp(corpus,topics):
    print "Started rp"
    tStart = time()
    rp = models.RpModel(corpus, num_topics=500, id2word=dictionary)
    tStop = time()
    print "Running time rp: %f" % (tStop - tStart)
    #rp.save('/Volumes/My Passport/gensim-wiki-ensimple/models/model.rp')
    pathrp = pathModelFolder + '/model.rp'
    rp.save(pathrp)


def gen_hdp(corpus):
    print "Started hdp"
    tStart = time()
    hdp = models.HdpModel(corpus, id2word=dictionary)
    tStop = time()
    print "Running time rp: %f" % (tStop - tStart)
    #hdp.save('/Volumes/My Passport/gensim-wiki-ensimple/models/model.hdp')
    pathhdp = pathModelFolder + '/model.hdp'
    hdp.save(pathhdp)

if __name__ == '__main__':
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
    tfidf = tfidf = models.TfidfModel.load(pathModelFolder+"/model.tfidf")
    corpus_tfidf = tfidf[corpus]

    pLsi1 = Process(target=gen_lda, args=(corpus_tfidf,50,'tfidf_noupdates_1pass',1))
    pLsi2 = Process(target=gen_lda, args=(corpus_tfidf,50,'tfidf_noupdates_20passes',20))


    #gen_lsi(corpus_tfidf, 500)
    #gen_lda(corpus_tfidf, 200,'tfidf_noupdates_20passes')

    #gen_rp(corpus_tfidf,500)
    #gen_hdp(corpus_tfidf)
    #gen_ldaMultiCore(corpus_tfidf, 500)






