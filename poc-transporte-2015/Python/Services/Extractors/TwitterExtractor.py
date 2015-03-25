'''
Created on 26/01/2015

@author: pcosta
'''
import pika
import codecs
import json
import sys
import pytz
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from collections import namedtuple
local_tz = pytz.timezone('America/Sao_Paulo')

class StdOutListener(StreamListener):
    def __init__(self, filtros):
        self.filatweets = []
        json_config=codecs.open("TwitterConfig.json","r")
        config = json.loads(json_config.read(), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        json_config.close();
        auth = OAuthHandler(config.twitter.consumer_key, config.twitter.consumer_secret)
        auth.set_access_token(config.twitter.access_token, config.twitter.access_token_secret)
        while True:
            try:
                stream = Stream(auth, self)
                #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
                stream.filter(track=filtros.split(','))
            except Exception as e:
                print e
                print "Reiniciando o servico"
                continue
        

    def on_data(self, data):
        try:
            print data
            if len(self.filatweets) > 25:
                self.filatweets.pop(0)
            self.filatweets.append(data)
            return True
        except Exception as e:
            print e
            
    def on_error(self, status):
        print status


def main():
    StdOutListener("manifestacao,paulista")
   
if __name__ == '__main__':
    main()
