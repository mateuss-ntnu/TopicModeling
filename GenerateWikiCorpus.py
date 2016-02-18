import re
import logging
import nltk
import os
from gensim import corpora
from time import time
import Tools


class GenerateCorpus:
    def __init__(self, article_files, dictionary):
        self.__list = article_files
        self._dictionary = dictionary

    def __iter__(self):
        for text in ParseWikiText(self.__list):
            yield self._dictionary.doc2bow(text.lower().split())


class ParseWikiText:
    def __init__(self, article_files):
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

                start_line_pattern = re.compile('<doc.*>')
                end_line_pattern = re.compile('</doc>')
                document_id_pattern = re.compile('<doc id="([^"]*)".*')
                if start_line_pattern.match(line):
                    self.listIDs.append(re.search(document_id_pattern, line).group(1))
                    text = ""
                    line = f.readline()
                    while line and not end_line_pattern.match(line):
                        text += line
                        line = f.readline()
                    # print text
                    yield text
                else:
                    line = f.readline()
            f.close()

    def get_ids(self):
        return self.listIDs


class GenerateWikiCorpus:
    def __init__(self, path_location, path_doc):
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

        self._pathLocation = path_location
        self._pathDictionary = path_location + "/dictionary.dict"
        self._pathCorpus = path_location + "/corpus.mm"
        self._pathDoc = path_doc
        self._pathBinding = path_location + "/corpus-docs.binding"

    def return_article_paths(self):
        articles = []
        if os.path.isdir(self._pathDoc):
            for (path, dirs, files) in os.walk(self._pathDoc):
                for fil in files:
                    if not str(fil).startswith('.'):
                        articles.append(str(path) + '/' + str(fil))
            return sorted(articles)
        else:
            articles.append(self._pathDoc)
            return articles

    def return_articles(self):
        articles = []

        os.chdir(self._pathDoc)
        paths_list = os.listdir(os.curdir)

        for directory in paths_list:

            if os.path.isdir(directory):
                sub_list = filter(lambda f: not f.startswith('.'), os.listdir(directory))
                articles.extend(sub_list)
                # return articles

        return articles



    def generate(self):
        # pathDictionary = '/Volumes/My Passport/gensim-wiki/dictionary.dict'
        # pathCorpus = '/Volumes/My Passport/gensim-wiki/corpus.mm'

        Tools.create_folder_if_not_exists(self._pathLocation)

        t_start = time()

        # Generate a list of files
        list_files = self.return_article_paths()

        iter_text = ParseWikiText(list_files)
        dictionary = corpora.Dictionary(text.lower().split() for text in iter_text)
        # remove stop words and words that appear only once

        ids = iter_text.get_ids
        ids = ids.im_self.listIDs

        stoplist = set(nltk.corpus.stopwords.words("english"))
        stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
        once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
        dictionary.filter_tokens(stop_ids + once_ids)  # remove stop words and words that appear only once
        dictionary.compactify()
        dictionary.save(self._pathDictionary)

        corpus = GenerateCorpus(list_files, dictionary)
        corpora.MmCorpus.serialize(self._pathCorpus, corpus)

        # Save index to file

        import pickle
        pickle.dump(ids, open(self._pathBinding, 'w'))

        # for i in range(0,len(ids)):
        #    print "{0}\t{1}".format(i,ids[i])

        t_end = time()

        print "Running time: %f" % (t_end - t_start)
