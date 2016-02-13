import os
import re
import pickle

pathDoc = "/Volumes/My Passport/wiki_ensimple-20160111/"
pathBinding = "/Volumes/My Passport/gensim-wiki-ensimple-20160111/corpus-docs.binding"


def getTitles(__list):
    for article_file in __list:
        print(article_file)
        f = open(article_file)
        line = f.readline()
        while line:
            # assume there's one document per line, tokens separated by whitespace
            # yield dictionary.doc2bow(line.lower().split())

            startLinePattern = re.compile('<doc.*>')
            endlinePattern = re.compile('</doc>')
            documentIdPattern = re.compile('<doc id="([^"]*)".*');
            documentTitlePattern = re.compile('<doc.*title="([^"]*)".*')
            documentUrlPattern = re.compile('<doc.*url="([^"]*)".*')
            if startLinePattern.match(line):
                #self.listIDs.append(re.search(documentIdPattern, line).group(1))
                title = re.search(documentTitlePattern, line).group(1)
                line = f.readline()
                yield title
                '''
                text = ""
                line = f.readline()
                while line and not endlinePattern.match(line):
                    text += line
                    line = f.readline()
                # print text
                yield text
                '''
            else:
                line = f.readline()
        f.close()

def getTitle(__list, id):

    for article_file in __list:
        #print(article_file)
        f = open(article_file)
        line = f.readline()
        while line:
            # assume there's one document per line, tokens separated by whitespace
            # yield dictionary.doc2bow(line.lower().split())
            if startLinePattern.match(line):
                if re.search(documentIdPattern, line).group(1) == id:
                    return re.search(documentTitlePattern, line).group(1)
                else:
                    line = f.readline()

            else:
                line = f.readline()
        f.close()




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

startLinePattern = re.compile('<doc.*>')
endlinePattern = re.compile('</doc>')
documentIdPattern = re.compile('<doc id="([^"]*)".*');
documentTitlePattern = re.compile('<doc.*title="([^"]*)".*')
documentUrlPattern = re.compile('<doc.*url="([^"]*)".*')

files = returnArticlePaths()
#titleGenerator = getTitles(files)
#for title in titleGenerator:
#    print title

binding = pickle.load(open(pathBinding,'r'))

for b in reversed(binding):
    print b +" - "+ getTitle(files, b)