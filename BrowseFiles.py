import os
import re

#pathDoc = '../wiki_en-20160113'
pathModel = "/Volumes/My Passport/gensim-wiki-ensimple-20160111"

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

def returnAllDirs():
    directories = []
    for (path, dirs, files) in os.walk(pathDoc):
        for dir in sorted(dirs):
            #if(not str(fil).startswith('.')):
            directories.append(str(path)+'/'+str(dir))
    return directories


def countArticleHierarcy(list):
    count = 0;
    for path in list:
        print(path)
        f = open(path)
        line = f.readline()
        while line:
            # assume there's one document per line, tokens separated by whitespace
            # yield dictionary.doc2bow(line.lower().split())
            startLinePattern = re.compile("<doc.*>")
            endlinePattern = re.compile("</doc>")
            if startLinePattern.match(line):
                count += 1
            line = f.readline()
        f.close()
    return count

def returnModelsWithEnding(list):
    articles = []
    if os.path.isdir(pathModel):
        for (path, dirs, files) in os.walk(pathModel):
            for fil in files:
                for s in list:
                    if(not str(fil).startswith('.') and str(fil).endswith(s)):
                        articles.append(str(path)+'/'+str(fil))
        return articles
    else:
        articles.append(pathModel)
        return articles



#articlesList = return_articles()
## print(returnArticlePaths())
#print(str(countArticleHierarcy(returnArticlePaths())))
#dirs = returnAllDirs()
#for dir in dirs:
#    print dir

endings = [".lsi",".lda",".rp",".hdp"]

articles = returnModelsWithEnding(endings)
for article in articles:
    print re.match(".*\/(.*)",article).group(1)



#i=0