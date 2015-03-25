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
import codecs
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
        if top in topicHandler.dictIgnore:
            ignoreWords = set(topicHandler.dictIgnore[top])
            inter = set.intersection(words, ignoreWords)
            if len(inter) > 0:
                return True

        return False

def checkCity(text):
    text = text.lower().replace("brasil","")
    global topicHandler
    global config
    lst = topicHandler.getWords(text.lower())
    words = set(lst)
    cities = set(config.cidades)
    return len(set.intersection(words, cities))>0 or text == ""

def processe(body):
    try:
        global lstTwitter
        global config
        global commit
        global topicHandler
        jsonBody = json.loads(body)
        print jsonBody['twitter_text']
        topicos = topicHandler.getTopicos(jsonBody['twitter_text'])
        if len(topicos) > 0:
            if jsonBody['location'] != None:
                if checkCity(jsonBody['location']):
                    checkIgnore = checkIgnoreWords(topicos, jsonBody['twitter_text'])
                    if not checkIgnore:
                        print "###############"
                        print topicos
                        print "###############"
                        lstTwitter.add(body)
                    else:
                        print "ignorando o tweet por palavras!"
                else:
                    print "ignorando tweet da cidade de:" + jsonBody['user']['location']
        else:
            print "não encontramos tópicos"
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
    solr = pysolr4.Solr(u'http://'+config.solr.server+':'+config.solr.port+'/solr/'+ config.solr.collection+"/")
    #start rabbit
    f = codecs.open("G:\\Poc-Transporte\\svn\\Poc-Transporte-2015\\Python\\Outputs\\RabbitTweetConsumerError.txt", "r", "utf-8")
    count = 0
    ccommit = 0
    try:
        for line in f.readlines():
            count += 1
            jsonBody = json.loads(line)

            topicos = topicHandler.getTopicos(jsonBody['twitter_text'])

            if len(topicos) > 0:
               if checkCity(jsonBody['city']):
                    checkIgnore = checkIgnoreWords(topicos, jsonBody['twitter_text'])
                    if not checkIgnore:
                        print topicos
                        print jsonBody['city']
                        print jsonBody['twitter_text']
                        print "###############"
                        ccommit += 1
                        #solr.update("",jsonBody).commit()
        print str(ccommit) + " de " + str(count)
    except Exception as e:
        print e
    f.close()

if __name__ == '__main__':
    main()
