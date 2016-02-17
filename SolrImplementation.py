import solr
import re
import os

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def genSolrIndex(__list):
    counter = 0
    for article_file in __list:
        #print(article_file)
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
                id = re.search(documentIdPattern,line).group(1)
                url = re.search(documentUrlPattern,line).group(1)
                line = f.readline()


                text = ""
                line = f.readline()
                while line and not endlinePattern.match(line):
                    text += line
                    line = f.readline()

                location = article_file.split("/")[-2]+"/"+article_file.split("/")[-1]

                doc = {
                    "id": id,
                    "title": title,
                    "url": url,
                    "location": location
                }


                counter+=1

                try:
                    s.add(doc)
                except:
                    print "error "+str(counter)+" "+title

                '''s.add(doc)'''
                #counter+=1
                print "Added "+str(counter)+" "+title

            else:
                line = f.readline()
        s.commit()
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


pathDoc = "/Volumes/My Passport/wiki_ensimple-20160111/"
s = solr.SolrConnection('http://localhost:8983/solr/simplewiki')






#files = returnArticlePaths()
#genSolrIndex(files)

response = s.query('title:"Ocean"')
hit = response.results[0]['title']
