from gensim import corpora, models, similarities

pathDictionary = '/Volumes/My Passport/gensim-wiki-ensimple-20160111/dictionary.dict'
pathCorpus = '/Volumes/My Passport/gensim-wiki-ensimple-20160111/corpus.mm'
pathIndex = '/Volumes/My Passport/gensim-wiki-ensimple-20160111/index.index'


corpus = corpora.MmCorpus(pathCorpus)
print corpus[20545]