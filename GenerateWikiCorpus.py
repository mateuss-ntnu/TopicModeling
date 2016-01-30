__author__ = 'Mateusz'

import re
import logging
import nltk

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

pathDictionary = ''
pathCorpus = ''
pathDoc = ''
pathBinding = ''

import sys

if sys.argv.__len__() == 5:
    pathDictionary = sys.argv[1]
    pathCorpus = sys.argv[2]
    pathDoc = sys.argv[3]
    pathBinding = sys.argv[4]

import os

def returnArticlePaths():
    articles = []
    if os.path.isdir(pathDoc):
        for (path, dirs, files) in os.walk(pathDoc):
            for fil in files:
                if(not str(fil).startswith('.')):
                    articles.append(str(path)+'/'+str(fil))
        return sorted(articles)
    else:
        articles.append(pathDoc)
        return articles

def returnArticles():
    articles = []

    os.chdir(pathDoc)
    list = os.listdir(os.curdir)

    for dir in list:

        if os.path.isdir(dir):
            sublist = filter(lambda f: not f.startswith('.'), os.listdir(dir))
            articles.extend(sublist)
            # return articles

    return articles


class GenerateWikiCorpus():
    def __init__(self,article_files):
        self.__list = article_files

    def __iter__(self):
        for text in ParseWikiText(self.__list):
            yield dictionary.doc2bow(text.lower().split())


class ParseWikiText():
    def __init__(self,article_files):
        self.__list = article_files
        self.listIDs = []

    def __iter__(self):
        for article_file in self.__list:
            print(article_file)
            f = open(article_file)
            line = f.readline()
            while line:
                # assume there's one document per line, tokens separated by whitespace
                # yield dictionary.doc2bow(line.lower().split())

                startLinePattern = re.compile('<doc.*>')
                endlinePattern = re.compile('</doc>')
                documentIdPattern = re.compile('<doc id="([^"]*)".*');
                if startLinePattern.match(line):
                    self.listIDs.append(re.search(documentIdPattern, line).group(1))
                    text = ""
                    line = f.readline()
                    while line and not endlinePattern.match(line):
                        text += line
                        line = f.readline()
                    # print text
                    yield text
                else:
                    line = f.readline()
            f.close()

    def getIDs(self):
        return self.listIDs


def countArticles(path):
    f = open(path)
    line = f.readline()
    count = 0;
    while line:
        # assume there's one document per line, tokens separated by whitespace
        # yield dictionary.doc2bow(line.lower().split())
        startLinePattern = re.compile("<doc.*>")
        endlinePattern = re.compile("</doc>")
        if startLinePattern.match(line):
            count + 1
    f.close()

def countArticleHierarcy(list):
    for path in list:
        f = open(path)
        line = f.readline()
        count = 0;
        while line:
            # assume there's one document per line, tokens separated by whitespace
            # yield dictionary.doc2bow(line.lower().split())
            startLinePattern = re.compile("<doc.*>")
            endlinePattern = re.compile("</doc>")
            if startLinePattern.match(line):
                count + 1
        f.close()


from gensim import corpora, models, similarities

# pathDictionary = '/Volumes/My Passport/gensim-wiki/dictionary.dict'
# pathCorpus = '/Volumes/My Passport/gensim-wiki/corpus.mm'


from time import time

tStart = time()

# Generate a list of files
listFiles = returnArticlePaths()

iterText = ParseWikiText(listFiles)
dictionary = corpora.Dictionary(text.lower().split() for text in iterText)
# remove stop words and words that appear only once

IDs = iterText.getIDs
IDs = IDs.im_self.listIDs

import nltk

stoplist = set(nltk.corpus.stopwords.words("english"))
stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
dictionary.filter_tokens(stop_ids + once_ids)  # remove stop words and words that appear only once
dictionary.compactify()
dictionary.save(pathDictionary)

corpus = GenerateWikiCorpus(listFiles)
corpora.MmCorpus.serialize(pathCorpus, corpus)

#Save index to file

import pickle
pickle.dump(IDs, open(pathBinding, 'w'));


#for i in range(0,len(IDs)):
#    print "{0}\t{1}".format(i,IDs[i])

tEnd = time()

print "Running time: %f" % (tEnd - tStart)

