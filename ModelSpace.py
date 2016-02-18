import logging
from gensim import corpora, models
import multiprocessing as mp
from time import time
import Tools

class ModelSpace:

    def __init__(self, path_location, num_topics):
        #pathDictionary = '/Volumes/My Passport/gensim-wiki-ensimple/dictionary.dict'
        #pathCorpus = '/Volumes/My Passport/gensim-wiki-ensimple/corpus.mm'

        self._pathDictionary = path_location + "/dictionary.dict"
        self._pathCorpus = path_location + "/corpus.mm"
        self._pathModelsFolder = path_location + "/models"
        self._num_topics = num_topics

        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

        self._dictionary = corpora.Dictionary.load(self._pathDictionary)
        self._corpus = corpora.MmCorpus(self._pathCorpus)
        print ('%s/model.rp') %(self._pathModelsFolder)

    def gen_tfidf(self, corpus):
        print "Started tfidf"
        tStart = time()
        tfidf = models.TfidfModel(corpus, normalize=True)
        tStop = time()
        print "Running time tfidf: %f" % (tStop - tStart)
        pathtfidf = self._pathModelsFolder + '/model.tfidf'
        tfidf.save(pathtfidf)
        return tfidf


    def gen_lsi(self, corpus,topics,comment):
        print "Started lsi "+comment+" "+str(topics)
        tStart = time()
        lsi = models.LsiModel(corpus, id2word=self._dictionary, num_topics=topics)
        tStop = time()
        print "Running time lsi "+comment+str(topics)+": %f" % (tStop - tStart)
        #lsi.save('/Volumes/My Passport/gensim-wiki-ensimple/models/model.lsi')
        pathlsi = self._pathModelsFolder + '/model-' + comment + '-' + str(topics) + '.lsi'
        lsi.save(pathlsi)

    def gen_lda(self, corpus,topics,comment):
        print "Started lda"+comment+" "+str(topics)
        tStart = time()
        lda = models.LdaModel(corpus=corpus, id2word=self._dictionary, update_every=1, num_topics=topics)
        tStop = time()
        print "Running time lda "+comment+str(topics)+": %f" % (tStop - tStart)
        pathlda = self._pathModelsFolder + '/model-' + comment + '-' + str(topics) + '.lda'
        lda.save(pathlda)

    def gen_ldaMultiCore(self, corpus,topics,comment):
        print "Started lda multicore"+comment+" "+str(topics)
        tStart = time()
        import multiprocessing as mp
        lda = models.LdaMulticore(corpus=corpus, id2word =self._dictionary, workers=(mp.cpu_count()/2-1), num_topics=topics)
        tStop = time()
        print "Running time lda multicore "+comment+str(topics)+": %f" % (tStop - tStart)
        pathldamulti = self._pathModelsFolder + '/model-' + comment + '-' + str(topics) + '.ldamulti'
        lda.save(pathldamulti)

    def gen_rp(self, corpus, topics, comment):
        print "Started rp "+comment+" "+str(topics)
        tStart = time()
        rp = models.RpModel(corpus, num_topics=topics, id2word=self._dictionary)
        tStop = time()
        print "Running time rp "+comment+str(topics)+": %f" % (tStop - tStart)
        #rp.save('/Volumes/My Passport/gensim-wiki-ensimple/models/model.rp')
        pathrp = self._pathModelsFolder + '/model-' + comment + '-' + str(topics) + '.rp'
        rp.save(pathrp)


    def gen_hdp(self,corpus,comment):
        print "Started hdp"+comment
        tStart = time()
        hdp = models.HdpModel(corpus, id2word=self._dictionary)
        tStop = time()
        print "Running time hdp "+comment+": %f" % (tStop - tStart)
        #hdp.save('/Volumes/My Passport/gensim-wiki-ensimple/models/model.hdp')
        pathhdp = self._pathModelsFolder + '/model-' + comment + '.hdp'
        hdp.save(pathhdp)



    def prepare_gen(self):
        Tools.create_folder_if_not_exists(self._pathModelsFolder)
        pathtfidf = self._pathModelsFolder + '/model.tfidf'
        #self._tfidf = self.gen_tfidf(self._corpus)
        self._tfidf = models.TfidfModel.load(pathtfidf)
        self._corpus_tfidf = self._tfidf[self._corpus]

    def gen_model_serial(self):
        self.prepare_gen()

        num_topics = [10, 20, 50, 100, 200]

        comment = "tfidf"
        self._gen_hdp(self._corpus_tfidf,comment)
        for n in num_topics:
            self._gen_lsi(self._corpus_tfidf, n, comment)
            self._gen_lda(self._corpus_tfidf, n, comment)
            #self._gen_ldaMultiCore(corpus_tfidf, n, comment)
            self._gen_rp(self._corpus_tfidf,n, comment)

        comment = "bow"
        self._gen_hdp(self._corpus,comment)
        for n in num_topics:
            self._gen_lsi(self._corpus, n, comment)
            self._gen_lda(self._corpus, n, comment)
            #self._gen_ldaMultiCore(corpus, n, comment)
            self._gen_rp(self._corpus,n, comment)




    def gen_model_pool(self, processes=2):
        self.prepare_gen()


        pool = mp.Pool(processes=2)



        comment = "tfidf"
        processes = []
        processes.append(pool.apply_async(self.gen_hdp, (self._corpus_tfidf, comment)))
        for n in self._num_topics:
            processes.append(pool.apply_async(self.gen_lsi, (self._corpus_tfidf, n, comment)))
            processes.append(pool.apply_async(self.gen_lda, (self._corpus_tfidf, n, comment)))
            processes.append(pool.apply_async(self.gen_rp, (self._corpus_tfidf, n, comment)))

        comment = "bow"
        processes.append(pool.apply_async(self.gen_hdp, (self._corpus, comment)))
        for n in self._num_topics:
            processes.append(pool.apply_async(self.gen_lsi, (self._corpus, n, comment)))
            processes.append(pool.apply_async(self.gen_lda, (self._corpus, n, comment)))
            processes.append(pool.apply_async(self.gen_rp, (self._corpus, n, comment)))

        pool.close()
        map(mp.pool.ApplyResult.wait, processes)


    def gen_model_processes(self):

        self.prepare_gen()
        processes = []

        comment = "tfidf"
        processes.append(mp.Process(target=self.gen_hdp, args=(self._corpus_tfidf, comment)))
        for n in self._num_topics:
            processes.append(mp.Process(target=self.gen_lsi, args=(self._corpus_tfidf, n, comment)))
            processes.append(mp.Process(target=self.gen_lda, args=(self._corpus_tfidf, n, comment)))
            processes.append(mp.Process(target=self.gen_rp, args=(self._corpus_tfidf, n, comment)))

        comment = "bow"
        processes.append(mp.Process(target=self.gen_hdp, args=(self._corpus, comment)))
        for n in self._num_topics:
            processes.append(mp.Process(target=self.gen_lsi, args=(self._corpus, n, comment)))
            processes.append(mp.Process(target=self.gen_lda, args=(self._corpus, n, comment)))
            processes.append(mp.Process(target=self.gen_rp, args=(self._corpus, n, comment)))

        for p in processes:
            p.start()

        #for p in processes:
            # p.join()







