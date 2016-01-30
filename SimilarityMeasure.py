import re
import logging
import nltk
import sys
from gensim import corpora, models, similarities

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


import sys

if sys.argv.__len__() == 3:
     pathDictionary =    sys.argv[1] +"/dictionary.dict"
     pathCorpus =        sys.argv[1] +"/corpus.mm"
     pathIndex =         sys.argv[1] +"/index.index"
     pathTFIDF =         sys.argv[1] +"/models/model.tfidf"
     pathLsi =           sys.argv[1] +"/models/model-tfidf50-.lsi"
     pathLda =           sys.argv[1] +"/models/model-tfidf50-.lda"
     pathBinding =       sys.argv[1] +"/corpus-docs.binding"
     query =             sys.argv[2]
else:
     print "pathFolder query"
     quit()
############################################################################################



#pathTFIDF = '/media/mateusz/My Passport/gensim-small-sample/models/model.tfidf'
#
#pathDictionary = '/media/mateusz/My Passport/gensim-small-sample/dictionary.dict'
#pathCorpus = '/media/mateusz/My Passport/gensim-small-sample/corpus.mm'
#pathIndex = '/media/mateusz/My Passport/gensim-small-sample/index.index'
#
#pathLsi = '/media/mateusz/My Passport/gensim-small-sample/models/model.lsi'
#pathLda = '/media/mateusz/My Passport/gensim-small-sample/models/model.lda'
#
#pathBinding = '/media/mateusz/My Passport/gensim-small-sample/corpus-docs.binding'

######################################################################################
#pathTFIDF = '/Volumes/My Passport/gensim-wiki-ensimple/models/model.tfidf'
#pathTFIDF = '/Volumes/My Passport/gensim-wiki-ensimple-20160111/models/model.tfidf'

#pathDictionary = '/Volumes/My Passport/gensim-wiki-ensimple-20160111/dictionary.dict'
#pathCorpus = '/Volumes/My Passport/gensim-wiki-ensimple-20160111/corpus.mm'
#pathIndex = '/Volumes/My Passport/gensim-wiki-ensimple-20160111/index.index'




#pathLsi = '/Volumes/My Passport/gensim-wiki-ensimple-20160111/models/model.lsi'
#pathLda = '/Volumes/My Passport/gensim-wiki-ensimple-20160111/models/model.lda'
########################################################################################
# pathLsi = '/Volumes/My Passport/gensim-wiki-ensimple/models/model.lsi'
# pathLsi2 = '/Volumes/My Passport/gensim-wiki-ensimple/models/model2.lsi'
# pathLsi3 = '/Volumes/My Passport/gensim-wiki-ensimple/models/model3.lsi'
# pathLsi100 = '/Volumes/My Passport/gensim-wiki-ensimple/models/model100.lsi'
#
# pathLsi10_tf = '/Volumes/My Passport/gensim-wiki-ensimple/models/model10_tf.lsi'
# pathLsi50_tf = '/Volumes/My Passport/gensim-wiki-ensimple/models/model50_tf.lsi'
# pathLsi100_tf = '/Volumes/My Passport/gensim-wiki-ensimple/models/model100_tf.lsi'
# pathLsi300_tf = '/Volumes/My Passport/gensim-wiki-ensimple/models/model300_tf.lsi'
#
# pathLda10 = '/Volumes/My Passport/gensim-wiki-ensimple/models/model10.lda'
# pathLda10_tf = '/Volumes/My Passport/gensim-wiki-ensimple/models/model10_tf.lda'
# pathLda50 = '/Volumes/My Passport/gensim-wiki-ensimple/models/model50.lda'
# pathLda50_tf = '/Volumes/My Passport/gensim-wiki-ensimple/models/model50_tf.lda'
#
# pathDictionary = '/Volumes/My Passport/gensim-wiki-ensimple/dictionary.dict'
# pathCorpus = '/Volumes/My Passport/gensim-wiki-ensimple/corpus.mm'
# pathIndex = '/Volumes/My Passport/gensim-wiki-ensimple/index.index'
################################################################################
#query = "Australia"


createIndex = True

corpus = corpora.MmCorpus(pathCorpus)
dictionary = corpora.Dictionary.load(pathDictionary)
tfidf = models.TfidfModel.load(pathTFIDF)

#lsi = models.LsiModel.load(pathLsi)

corpus_tfidf = tfidf[corpus]

lsi = models.LsiModel.load(pathLsi)
lda = models.LdaModel.load(pathLda)

query_bow = dictionary.doc2bow(query.lower().split())
query_lsi = lsi[query_bow]
query_lda = lda[query_bow]

if(createIndex):
    index = similarities.MatrixSimilarity(lda[corpus])
    index.save(pathIndex)
else:
    index = similarities.Similarity.load(pathIndex)
print ' '

sims = index[query_lda] # perform a similarity query against the corpus
sims = sorted(enumerate(sims), key=lambda item: -item[1])
#print(sims)

import pickle
binding = pickle.load(open(pathBinding,'r'))

for i in range(0,15):
    print "{0}\t\t->\t{1}".format(sims[i],binding[sims[i][0]])

#for i in range(0,len(binding)):
#    print "{0}\t{1}".format(i,binding[i])



#topics =lsi.show_topics(num_topics=-1, num_words=-1, log=False, formatted=True)
#topics_lsi = lsi.print_topics(-1)
print ' '
#topics_lda = lda.print_topics(-1)

