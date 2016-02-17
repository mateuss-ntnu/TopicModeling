__author__ = 'Mateusz'

from urllib2 import *
conn = urlopen('http://localhost:8983/solr/wikiensimple/select?q=iPod&wt=python')
import ast
rsp = ast.literal_eval(conn.read())

print "number of matches=", rsp['response']['numFound']

#print out the name field for each returned document
for doc in rsp['response']['docs']:
  print doc['title']
  print doc['text']
  print "##################"