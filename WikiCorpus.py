__author__ = 'Mateusz'

import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim.corpora import Dictionary, HashDictionary, MmCorpus, WikiCorpus
from gensim.models import TfidfModel


wiki = WikiCorpus("/Users/Mateusz/Desktop/gensim-wiki/enwiki-20150805-pages-articles-multistream.xml.bz2")
MmCorpus.serialize("/Users/Mateusz/Desktop/gensim-wiki")