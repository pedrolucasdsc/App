#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      llima
#
# Created:     23/02/2015
# Copyright:   (c) llima 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pika
import codecs
import json
import sys
import pysolr4, pymongo, unirest, time, datetime
from threading import Thread
from bs4 import BeautifulSoup as Soup
from collections import namedtuple
from time import mktime
sys.argv.append("RSSConfig.json")
sys.path.append("G:\\Poc-Transporte\\svn\\Poc-Transporte-2015\\Python\\Utilities")
from TopicHandler import TopicHandler
from reviewParser import parseReviews
docs = []
config = ""

class thProcessAndCommit(Thread):
    def __init__ (self,docs, arqConfig):
        Thread.__init__(self)
        self.docs = docs
        self.config = arqConfig
        #conexão solr
        self.solr = pysolr4.Solr(u'http://'+arqConfig.solr.server+':'+arqConfig.solr.port+'/solr/'+ arqConfig.solr.collection+"/")
        #conexão mongo
        connection = pymongo.Connection(u"mongodb://" + arqConfig.mongodb.server, safe=True)
        self.db = connection[arqConfig.mongodb.database]
        self.rssDocuments = self.db[arqConfig.mongodb.collection]
        self.TopicHandler = TopicHandler(arqConfig)

    def ExtractorElementWebPage(self, jsonFind):

        return unirest.post("http://" + self.config.ExtractorElementWebPageApi.server + ":" + self.config.ExtractorElementWebPageApi.port + "/" + self.config.ExtractorElementWebPageApi.title,
            headers = { "Accept" : "application/json", "Content-Type": "application/json"},
            params = json.dumps(jsonFind)
    )

    def getRss(self, doc):
        for r in self.config.rss:
            if  r.name.encode('utf8').lower() in doc['link']:
                return r


    def getMetroNewsDocument(self, content):
        soup = Soup(content)
        listP = soup.findAll(text=True)
        return ''.join(listP)

    def getDocument(self, url, rss):
        print "get document: " + url
        myjson = {"urlWebPage":url, "find":rss.find, "text":True}
        ret = self.ExtractorElementWebPage(myjson)
        text = ''.join(ret.body['element'])
        return text
    def normalizeReviews(self, doc):
        doc['num_reviews'] = len(doc['reviews'])
        doc['reviews_ids'] = []
        doc['reviews_interact_dislikes']=[]
        doc['reviews_interact_likes']=[]
        doc['reviews_str_data'] = []
        doc['reviews_user_info_link'] =[]
        doc['reviews_user_info_name'] =[]
        for r in doc['reviews']:
            for rr in r:
                doc['reviews_ids'].append(rr['data_id'])
                doc['reviews_interact_dislikes'].append(rr['interact']['dislikes'])
                doc['reviews_interact_likes'].append(rr['interact']['likes'])
                doc['reviews_str_data'].append(rr['str_data'])
                doc['reviews_user_info_link'].append(rr['user_info']['link'])
                doc['reviews_user_info_name'].append(rr['user_info']['name'])
        del doc['reviews']
    def setReviews(self, docs, review, rss_name):
        # extraindo todos os comentários da primeira página
        print "extraindo os comentarios"
        reviews =[]
        if rss_name == "METRONEWS":
            for doc in docs:
                if 'slash_comments' in doc:
                    doc['num_reviews'] = int(doc['slash_comments'])
                    del doc['slash_comments']
                if 'comments' in doc:
                    #review.url = doc['comments']
                    del doc['comments']
        else:
            myjson = {"urlWebPage":review.url, "find":review.find, "text":False}

            url_reviews = self.ExtractorElementWebPage(myjson)
            soup = Soup(''.join(url_reviews.body['element']))
            dictReviews = {}
            for a in soup.findAll('a'):
                dictReviews[a.text] = a.attrs["href"]
            count = len(docs)

            for doc in docs:
                if doc["title"] in dictReviews:
                    # buscar os comentários:
                    myjson = {"urlWebPage":dictReviews[doc["title"]], "find":review.find_review, "text":False}
                    print myjson

                    reviews = self.ExtractorElementWebPage(myjson)
                    jsonReviews = parseReviews(''.join(reviews.body['element']), rss_name)
                    doc["reviews"].append(jsonReviews)

        return reviews

    def run(self):
        # extraindo os topicos
        try:
            docsMongo =[]
            docsSolr = []
            handler = TopicHandler(self.config)
            for doc in docs:
                rss = self.getRss(doc)
                doc['reviews'] =[]
                doc['source'] = rss.name
            # extraindo os comentarios se existir sessão de comentarios
            for rss in self.config.rss:
                if hasattr(rss, 'review'):
                    docs_by_rss = [doc for doc in docs if doc['source'] == rss.name]
                    self.setReviews(docs_by_rss, rss.review, rss.name)

            for doc in docs:
                try:
                    rss = self.getRss(doc)
                    if 'links' in doc:
                        del doc['links']
                    if 'summary_detail' in doc:
                        del doc['summary_detail']
                    if 'title_detail' in doc:
                        del doc['title_detail']
                    if 'tags' in doc:
                        del doc['tags']

                    doc['id'] = doc['link']
                    doc['source'] = rss.name
                    if rss.name == "METRONEWS":
                        if 'content' in doc:
                            strContent = ''
                            for c in doc['content']:
                                strContent += c['value']
                            doc['document'] = self.getMetroNewsDocument(strContent)
                        del doc['content']
                        if 'author_detail' in doc:
                            del doc['author_detail']
                        if 'wfw_commentrss' in doc:
                            del doc['wfw_commentrss']
                        if 'authors' in doc:
                            del doc['authors']
                        if 'guidislink' in doc:
                            del doc['guidislink']
                    else:
                        doc['document'] = self.getDocument(doc['link'], rss)
                    doc['topic'] = handler.getTopicos(doc['title']+ "\n" + doc['document'])


                    # parse date
                    published =""
                    updated =""
                    docMongo = doc.copy()
                    if 'published' in doc:
                        published = doc['published']
                        docMongo['published'] = datetime.datetime.fromtimestamp(mktime(time.strptime(doc['published'],"%d/%m/%Y %H:%M:%S")))
                        doc['published'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.strptime(published,"%d/%m/%Y %H:%M:%S"))

                    if 'updated' in doc:
                        updated = doc['updated']
                        docMongo['updated'] = datetime.datetime.fromtimestamp(mktime(time.strptime(doc['updated'],"%d/%m/%Y %H:%M:%S")))
                        doc['updated'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.strptime(updated,"%d/%m/%Y %H:%M:%S"))
                    docsMongo.append(docMongo)
                    if len(doc['reviews']) > 0:
                        self.normalizeReviews(doc)
                    docsSolr.append(doc)
                except Exception as e:
                    print e

                # extraindo o sentimento

                # extraindo o resumo

                # extraindo as entidades nomeadas



            #excluindo campos desnecessários

            print "inserindo documentos no solr..."
            for d in docsSolr:
                try:
                    self.solr.update("?update.chain=mychain", d)
                    self.solr.commit()
                except Exception as e:
                    print e
                    self.saveDocWithErrors(d)
            #inserindo no mongo
            print "inserindo documentos no mongo"
            for d in docsMongo:
                try:
                    self.rssDocuments.insert(d)
                except Exception as e:
                    print e
                #self.rssDocuments.update({"id":d["id"]}, d, upsert =True)


            print "documentos inseridos."
        except Exception as e:
            print e


    def saveDocWithErrors(self, doc):
        f = open(doc['title']+".txt", "w")
        f.write(json.dumps(doc))
        f.close()

def callback(ch, method, properties, body):
    global docs
    global commit
    global config
    print body
    #return
    try:
        docs.append(json.loads(body))
        if(len(docs) >= int(config.rabbit.lenghtOfListCommit)):
            commit = thProcessAndCommit(docs, config)
            commit.run()
            docs=[]


    except Exception as e:
        docs=[]


def main():
    #Lê arquivo config
    json_config=codecs.open(sys.argv[1], "r", "utf-8")
    global config
    config = json.loads(json_config.read(), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    json_config.close();

    #start rabbit
    connectionRabbit = pika.BlockingConnection(pika.ConnectionParameters(str(config.rabbit.server)))
    channel = connectionRabbit.channel()
    channel.queue_declare(queue=config.rabbit.queue, durable=True)
    channel.basic_consume(callback,queue=config.rabbit.queue, no_ack=True)
    print ' [*] Waiting for messages. To exit press CTRL+C'
    channel.start_consuming()

if __name__ == '__main__':
    main()
