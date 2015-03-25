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
import pysolr4
def getSolrQuery(solr, query, register_per_page, fq):

    results = solr.select( ( 'q', query ),
                       ( 'fq', fq ),
                       ( 'rows', register_per_page ))


    docs = results.docs
    hits = results.response['numFound']
    start = len(docs)
    while start < hits:
        results = solr.select( ( 'q', query ),
                       ( 'fq', fq ),
                       ( 'rows', register_per_page ))
        print (str(start) + " - " + str(hits))
        docs += results.docs
        start = len(docs)

    return docs
def updateReach(docs, value):
    for d in docs:
        d['reach'] =value

    return docs

def setReachToMinus1():
    solr = pysolr.Solr('http://177.70.97.79:8983/solr/sptrans/', timeout=10)
    register_per_page = 1500
    #FLAG reach to -1
    query = '*:*'
    docs = getSolrQuery(solr, query, register_per_page)
    docs = updateReach(docs, -1)
    print("writting...." + str(len(docs)))
    tempdocs = []
    for d in docs:

        tempdocs.append(d)
        if len(tempdocs) == 1000:
            solr.add(tempdocs)
            print("writting + 1000")
            tempdocs = []
    solr.add(tempdocs)
    print("writting + " + str(len(tempdocs)))
    print("Done...")

def removeEntities(docs):
    for d in docs:
        remove_list = ['URL','RT', 'USR']
        word_list = d['pre_process_text'].split(' ')
        d['key'] = ' '.join([i for i in word_list if i not in remove_list])
    return docs

def calculateReach(docs):
    dict = {}
    for d in docs:
        if 'user_followers_count' in d:
            if d['key'] in dict:
                dict[d['key']] += d['user_followers_count']
            else:
                dict[d['key']] = d['user_followers_count']
        else:
            del d['key']
    return dict;
def main():
    solr = pysolr4.Solr('http://177.70.97.79:8983/solr/sptrans/')
    register_per_page = 1500
    #FLAG reach to -1
    query = 'pre_process_text:*'
    fq= 'creation_date_YEAR_MONTH_DAY:2015-03-05'
    docs = getSolrQuery(solr, query, register_per_page, fq)
    print('remove entities...')
    docs = removeEntities(docs)
    print ('calculating reaches')
    dictReach = calculateReach(docs)
    print("writting reaches...." + str(len(docs)))
    tempdocs = []
    for d in docs:
        del d['text']
        del d['_version_']
        if 'key' in d:
            d['reach'] = dictReach[d['key']]
            del d['key']
        tempdocs.append(d)
        if len(tempdocs) == 1000:
            solr.update(tempdocs)
            print("writting + 1000 reaches")
            tempdocs = []
    solr.update("",docs).commit()
    print("writting + " + str(len(tempdocs)))
    print("Done...")
if __name__ == '__main__':
    main()
