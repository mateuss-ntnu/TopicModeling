import GenerateWikiCorpus as gwp
import ModelSpace as ms


pathLocation = "/Volumes/My Passport/tmp/test-wiki"
pathDoc = "/Volumes/My Passport/wiki_ensimple-20160111"

#gen_wiki = gwp.GenerateWikiCorpus(pathLocation, pathDoc)
#gen_wiki.generate()

model_space = ms.ModelSpace(pathLocation, [10, ])


#model_space.gen_model_processes()
if __name__ == '__main__':
    model_space.gen_model_pool(3)
