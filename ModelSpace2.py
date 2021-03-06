__author__ = 'Mateusz'

import re
import logging
import nltk
import sys
import os

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
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=topics)
    tStop = time()
    print "Running time lsi "+comment+str(topics)+": %f" % (tStop - tStart)
    #lsi.save('/Volumes/My Passport/gensim-wiki-ensimple/models/model.lsi')
    pathlsi = pathModelFolder + '/model-'+comment+'-'+str(topics)+'.lsi'
    lsi.save(pathlsi)

def gen_lda(corpus,topics,comment):
    print "Started lda"+comment+" "+str(topics)
    tStart = time()
    lda = models.LdaModel(corpus=corpus, id2word=dictionary, update_every=1, num_topics=topics)
    tStop = time()
    print "Running time lda "+comment+str(topics)+": %f" % (tStop - tStart)
    pathlda = pathModelFolder + '/model-'+comment+'-'+str(topics)+'.lda'
    lda.save(pathlda)

def gen_ldaMultiCore(corpus,topics,comment):
    print "Started lda multicore"+comment+" "+str(topics)
    tStart = time()
    import multiprocessing as mp
    lda = models.LdaMulticore(corpus=corpus, id2word =dictionary, workers=2, num_topics=topics)
    tStop = time()
    print "Running time lda multicore "+comment+str(topics)+": %f" % (tStop - tStart)
    pathldamulti = pathModelFolder + '/model-'+comment+'-'+str(topics)+'.ldamulti'
    lda.save(pathldamulti)

def gen_rp(corpus, topics, comment):
    print "Started rp "+comment+" "+str(topics)
    tStart = time()
    rp = models.RpModel(corpus, num_topics=topics, id2word=dictionary)
    tStop = time()
    print "Running time rp "+comment+str(topics)+": %f" % (tStop - tStart)
    #rp.save('/Volumes/My Passport/gensim-wiki-ensimple/models/model.rp')
    pathrp = pathModelFolder + '/model-'+comment+'-'+str(topics)+'.rp'
    rp.save(pathrp)


def gen_hdp(corpus,comment):
    print "Started hdp"+comment
    tStart = time()
    hdp = models.HdpModel(corpus, id2word=dictionary)
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

from gensim import corpora, models

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

import multiprocessing as mp

    #for hypethreaded procs
    #pool =  mp.Pool(processes=(mp.cpu_count()/2-1))


comment = "bow"
gen_ldaMultiCore(corpus,500,comment)

'''
if __name__ == '__main__':
    pool = mp.Pool(processes=2)


    #num_topics = [10, 20, 50, 100, 200]#

    #comment = "tfidf"
    #pool.apply_async(gen_lda, (corpus_tfidf, 200, comment))
    comment = "bow"
    pool.apply_async(gen_rp, (corpus, 500, comment))
    pool.apply_async(gen_lda, (corpus, 500, comment))
    pool.apply_async(gen_lsi, (corpus, 500, comment))

    pool.close()
    pool.join()
'''
'''
    pool.apply_async(gen_hdp, (corpus_tfidf, comment))
    for n in num_topics:
        pool.apply_async(gen_lsi, (corpus_tfidf, n, comment))
        pool.apply_async(gen_lda, (corpus_tfidf, n, comment))
        pool.apply_async(gen_rp, (corpus_tfidf, n, comment))

    comment = "bow"
    pool.apply_async(gen_hdp, args=(corpus, comment))
    for n in num_topics:
        pool.apply_async(gen_lsi, args=(corpus, n, comment))
        pool.apply_async(gen_lda, args=(corpus, n, comment))
        pool.apply_async(gen_rp, args=(corpus, n, comment))
'''




'''
if __name__ == '__main__':
    processes = []

    num_topics = [10, ]#20, 50, 100, 200

    comment = "tfidf"
    processes.append(mp.Process(target=gen_hdp, args=(corpus_tfidf, comment)))
    for n in num_topics:
        processes.append(mp.Process(target=gen_lsi, args=(corpus_tfidf, n, comment)))
        processes.append(mp.Process(target=gen_lda, args=(corpus_tfidf, n, comment)))
        processes.append(mp.Process(target=gen_rp, args=(corpus_tfidf, n, comment)))

    comment = "bow"
    processes.append(mp.Process(target=gen_hdp, args=(corpus, comment)))
    for n in num_topics:
        processes.append(mp.Process(target=gen_lsi, args=(corpus, n, comment)))
        processes.append(mp.Process(target=gen_lda, args=(corpus, n, comment)))
        processes.append(mp.Process(target=gen_rp, args=(corpus, n, comment)))

    for p in processes:
        p.start()

    for p in processes:
        p.join()



'''
'''
num_topics = [10, 20, 50, 100, 200]

comment = "tfidf"
gen_hdp(corpus_tfidf,comment)
for n in num_topics:
    gen_lsi(corpus_tfidf, n, comment)
    gen_lda(corpus_tfidf, n, comment)
    #gen_ldaMultiCore(corpus_tfidf, n, comment)
    gen_rp(corpus_tfidf,n, comment)

comment = "bow"
gen_hdp(corpus,comment)
for n in num_topics:
    gen_lsi(corpus, n, comment)
    gen_lda(corpus, n, comment)
    #gen_ldaMultiCore(corpus, n, comment)
    gen_rp(corpus,n, comment)



'''


#comment = "tfidf"
#gen_lda(corpus_tfidf, 200, comment)


