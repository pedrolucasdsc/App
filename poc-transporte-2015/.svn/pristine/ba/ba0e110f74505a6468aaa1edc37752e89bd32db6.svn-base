#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      llima
#
# Created:     21/01/2015
# Copyright:   (c) llima 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#from pymongo import Connection
#connection = Connection("177.70.97.79")
#db = connection.sptrans
import pysolr
from bs4 import BeautifulSoup
def getSolrQuery(solr, query, register_per_page):
    results = solr.search(query, rows=register_per_page)
    docs = results.docs
    hits = results.hits
    start = len(docs)
    while start < hits:
        results = solr.search(query, rows=register_per_page, start=start)
        print (str(start) + " - " + str(hits))
        docs += results.docs
        start = len(docs)
        break
    return docs
def updateSource(docs):
    for d in docs:
        try:
            soup = BeautifulSoup(d['source'])
            d['source_text'] = soup.find('a').contents[0]
        except:
            print('error')
            d['source_text'] = "error"
    return docs


def main():
    solr = pysolr.Solr('http://177.70.97.79:8983/solr/sptrans', timeout=10)
    register_per_page = 1500
    #FLAG reach to -1
    query = 'source:*'
    docs = getSolrQuery(solr, query, register_per_page)
    docs = updateSource(docs)
    print("writting sources...." + str(len(docs)))
    tempdocs = []
    for d in docs:
        tempdocs.append(d)
        if len(tempdocs) == 1000:
            solr.add(tempdocs)
            print("writting + 1000 sources")
            tempdocs = []
    solr.add(tempdocs)
    print("writting + " + str(len(tempdocs)))
    print("Done...")
if __name__ == '__main__':
    main()
