__author__ = 'Mateusz'

import re
import logging
import nltk

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

pathDictionary = ''
pathCorpus = ''
pathDoc = ''

import sys

if sys.argv.__len__() == 4:
    pathDictionary = sys.argv[1]
    pathCorpus = sys.argv[2]
    pathDoc = sys.argv[3]


class GenerateWikiCorpus(object):

   def __iter__(self):
        for text in ParseWikiText():
             yield dictionary.doc2bow(text.lower().split())


class ParseWikiText(object):

   def __iter__(self):
        f = open(pathDoc)
        line = f.readline()
        while line:
            # assume there's one document per line, tokens separated by whitespace
            #yield dictionary.doc2bow(line.lower().split())

            startLinePattern = re.compile("<doc.*>")
            endlinePattern = re.compile("</doc>")
            if startLinePattern.match(line):
                text = ""
                line = f.readline()
                while not endlinePattern.match(line):
                    text += line
                    line = f.readline()
                #print text
                yield text
            else:
                line = f.readline()
        f.close()

def countArticles(path):
    f = open(path)
    line = f.readline()
    count = 0;
    while line:
        #assume there's one document per line, tokens separated by whitespace
        #yield dictionary.doc2bow(line.lower().split())
        startLinePattern = re.compile("<doc.*>")
        endlinePattern = re.compile("</doc>")
        if startLinePattern.match(line):
            count +1
    f.close()





from gensim import corpora, models, similarities


#pathDictionary = '/Volumes/My Passport/gensim-wiki/dictionary.dict'
#pathCorpus = '/Volumes/My Passport/gensim-wiki/corpus.mm'


from time import time
tStart = time()

dictionary = corpora.Dictionary(text.lower().split() for text in ParseWikiText())
# remove stop words and words that appear only once
import nltk
stoplist = set(nltk.corpus.stopwords.words("english"))
stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
dictionary.filter_tokens(stop_ids + once_ids) # remove stop words and words that appear only once
dictionary.compactify()
dictionary.save(pathDictionary)

corpus = GenerateWikiCorpus()
corpora.MmCorpus.serialize(pathCorpus, corpus)
tEnd = time()

print "Running time: %f" %(tEnd-tStart)

