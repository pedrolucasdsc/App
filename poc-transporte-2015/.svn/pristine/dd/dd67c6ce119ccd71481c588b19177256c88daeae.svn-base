'''
Created on 26/01/2015

@author: pcosta
'''
import copy
import pika
import codecs
from tweepy.streaming import StreamListener
import json
import pymongo
import sys
from collections import namedtuple
import pysolr4
import pytz

from threading import Thread
from Aelius import Toqueniza, Chunking
import re
sys.argv.extend(['TwitterConfig.json'])
local_tz = pytz.timezone('America/Sao_Paulo')
lstTwitter = None
commit = None
config = None

json_config=codecs.open(sys.argv[1],"r", "utf8")
config = json.loads(json_config.read(), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
json_config.close();
encontrou = False
for pathConfig in config.pathRootFolder:
    encontrou = False
    for path in sys.path:
        if path == pathConfig:
            encontrou = True
            break
    if not encontrou:
        sys.path.append(pathConfig)

from TweetSolrDocument import TweetSolrDocument
from TopicHandler import TopicHandler
topicHandler = TopicHandler(config)

class ListObjTwitter(StreamListener):
    def __init__(self, arqConfig):
        self.lstobjTwetter = {"solr":[], "mongo":[]};
        self.arqConfig = arqConfig
        return

    def len(self):
        return len(self.lstobjTwetter["solr"])

    def getList(self):
        return copy.copy(self.lstobjTwetter)

    def clear(self):
        self.lstobjTwetter  = {"solr":[], "mongo":[]};
        return

    def add(self, data):
        try:
            tweet = json.loads(data)
            tweet['filters'] = self.arqConfig.twitter.filters
            solrDoc = TweetSolrDocument(tweet, self.arqConfig)

            solr = {
                "id":solrDoc.id,
                "hashtags":solrDoc.hashtags,
                "reply_to_user_id":solrDoc.reply_to_user_id,
                "reply_to_screen_name":solrDoc.reply_to_screen_name,
                "reply_to_status_id":solrDoc.reply_to_status_id,
                "location":solrDoc.location.reverse(),
                "latitude":solrDoc.latitude,
                "longitude":solrDoc.longitude,
                "cd_geocodd":solrDoc.geocodd,
                "city":solrDoc.city,
                "number_of_retweets":solrDoc.number_of_retweets,
                "source":solrDoc.source,
                "sender_user_id":solrDoc.sender_user_id,
                "sender_screen_name":solrDoc.sender_screen_name,
                "sender_name":solrDoc.sender_name,
                "is_favorited":solrDoc.is_favorited,
                "is_retweet":solrDoc.is_retweet,
                "url_user_image": solrDoc.url_user_image,
                "url_entities_list":solrDoc.url_entities_list,
                "user_mention_list":solrDoc.user_mention_list,
                "user_mention_screen_name":solrDoc.user_mention_screen_name,
                "user_followers_count":solrDoc.user_followers_count,
                "user_statuses_count":solrDoc.user_statuses_count,
                "creation_date": solrDoc.creation_date,
                "filters": solrDoc.filters,
                "twitter_text": solrDoc.raw_text,
                "pre_process_text":solrDoc.text,
                "reach":solrDoc.reach,
                "sentiment":solrDoc.sentiment,
                "float_sentiment":solrDoc.float_sentiment,
                "sentimentB":solrDoc.sentimentB,
                "sentimentC":solrDoc.sentimentC,
                "topico": solrDoc.topico,
                "source_text":solrDoc.source_text,
                "image_face_recognition":solrDoc.image_face_recognition,
                "user_gender":solrDoc.user_gender,
                "user_age":solrDoc.user_age,
                "user_age_range":solrDoc.user_age_range,
                "creation_date_DAY":solrDoc.creation_date_DAY,
                "creation_date_HOUR":solrDoc.creation_date_HOUR,
                "creation_date_MONTH":solrDoc.creation_date_MONTH,
                "creation_date_YEAR":solrDoc.creation_date_YEAR,
                "creation_date_YEAR_MONTH":solrDoc.creation_date_YEAR_MONTH,
                "creation_date_YEAR_MONTH_DAY":solrDoc.creation_date_YEAR_MONTH_DAY,
                "creation_date_YEAR_MONTH_DAY_HOUR":solrDoc.creation_date_YEAR_MONTH_DAY_HOUR,
                #"filters":[]
                }

            self.lstobjTwetter['solr'].append(solr);
            self.lstobjTwetter['mongo'].append(tweet);

            #print(solrDoc.raw_text.encode("utf8"))
            return True

        except Exception as inst:
            print (type(inst))
            print (inst.args)
            return False

#--------------------------------------------------------------------------------------------1

class thCommit(Thread):


    def __init__ (self,lstObjTwetter, arqConfig):
        Thread.__init__(self)
        self.lstObjTwetter = lstObjTwetter
        #conexão solr
        self.solr = pysolr4.Solr(u'http://'+arqConfig.solr.server+':'+arqConfig.solr.port+'/solr/'+ arqConfig.solr.collection+"/")
        #conexão mongo
        connection = pymongo.Connection("mongodb://" + arqConfig.mongodb.server, safe=True)
        self.db = connection[arqConfig.mongodb.database]
        self.tweets = self.db[arqConfig.mongodb.collection]
        self.distritos = self.db['spatial'].find({"properties.type_json":"layer_distritos_sao_paulo"})
        self.TopicHandler = TopicHandler(arqConfig)

    def getGeoCodd(self, latitude, longitude):
        geocodd = -1
        distrito = "outros";
        self.db['temp'].insert({"loc": [latitude, longitude]})
        for d in self.distritos:
            loc = self.db['temp'].find({"loc":{"$geoWithin":{"$geometry" :{"type":"Polygon", "coordinates": d['geometry']['coordinates']}}}});
            for l in loc:
                print "Municipio:" + d['properties']['NM_DISTRIT']
                geocodd = d['properties']['CD_GEOCODD']
                distrito = d['properties']['NM_DISTRIT']
                self.db['temp'].remove({});
                return geocodd, distrito;
        self.db['temp'].remove({});
        return geocodd, distrito;


    def run(self):
        try:
            self.tweets.insert(self.lstObjTwetter["mongo"])
            for doc in self.lstObjTwetter["solr"]:
                doc["topico"] = self.TopicHandler.getTopicos(doc["twitter_text"].decode('utf-8'))
                doc["distrito"] = "outros"
                if doc['latitude'] != None:
                    doc['cd_geocodd'], doc["distrito"] = self.getGeoCodd(doc['latitude'], doc['longitude'])

            self.solr.update("",self.lstObjTwetter["solr"]).commit()

        except Exception as e:
            f = codecs.open("../../Outputs/RabbitTweetConsumerError.txt", "a", "utf-8")
            for d in self.lstObjTwetter["solr"]:
                f.write(json.dumps(d) + "\n");

            f.close()


def checkIgnoreWords(topicos, text):

    global topicHandler
    words = set(topicHandler.getWords(text.lower()))
    words_normal =set(topicHandler.getWords(text))
    for top in topicos:
        if top in topicHandler.dictSiglas:
            igonoreSiglas = set(topicHandler.dictSiglas[top])
            inters = set.intersection(igonoreSiglas, words_normal)
            if len(inters) > 0:
                return True
        if top in topicHandler.dictIgnore[top]:
            ignoreWords = set(topicHandler.dictIgnore[top])
            inter = set.intersection(words, ignoreWords)
            if len(inter) > 0:
                return True

        return False

def checkCity(text):
    global topicHandler
    global config
    words = set(topicHandler.getWords(text.lower()))
    cities = set(config.cidades)
    return len(set.intersection(words, cities))>0 or text == ""

def callback(ch, method, properties, body):
    try:
        global lstTwitter
        global config
        global commit
        global topicHandler
        jsonBody = json.loads(body)
        print jsonBody['text']
        topicos = topicHandler.getTopicos(jsonBody['text'])
        if len(topicos) > 0:
            if checkCity(jsonBody['user']['location']):
                checkIgnore = checkIgnoreWords(topicos, jsonBody['text'])
                if not checkIgnore:
                    print "###############"
                    print topicos
                    print "###############"
                    lstTwitter.add(body)
                else:
                    print u"ignorando o tweet por palavras!"
            else:
                print u"ignorando tweet da cidade de:" + jsonBody['user']['location']
        else:
            print u"não encontramos tópicos"
        if(lstTwitter.len() >= int(config.rabbit.lenghtOfListCommit)):
            commit.lstObjTwetter = lstTwitter.lstobjTwetter
            commit.run()
            lstTwitter.clear()
    except Exception as e:
        print e

def main():
    #Lê arquivo config
    global config
    global lstTwitter
    lstTwitter = ListObjTwitter(config)
    global commit
    commit = thCommit(lstTwitter.lstobjTwetter, config)
    #start rabbit
    while True:
        try:
            connectionRabbit = pika.BlockingConnection(pika.ConnectionParameters(str(config.rabbit.server)))
            channel = connectionRabbit.channel()
            channel.queue_declare(queue=config.rabbit.queue, durable=True)
            channel.basic_consume(callback,queue=str(config.rabbit.queue), no_ack=True)
            print ' [*] Waiting for messages. To exit press CTRL+C'
            channel.start_consuming()
        except Exception as e:
            print e
            print "Reiniciando o serviço"
            continue

if __name__ == '__main__':
    main()
