import os
import re

pathDoc = '../wiki_en-20160113'

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

#articlesList = return_articles()
## print(returnArticlePaths())
#print(str(countArticleHierarcy(returnArticlePaths())))
dirs = returnAllDirs()
for dir in dirs:
    print dir

articles = returnArticlePaths()
for article in articles:
    print article



#i=0