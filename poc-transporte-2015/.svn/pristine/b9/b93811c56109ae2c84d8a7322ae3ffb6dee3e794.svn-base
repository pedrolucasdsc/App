# -*- coding: utf-8 -*-
from pymongo import Connection
import pysolr
connection = Connection("177.70.97.184")
db = connection.sptrans
solr = pysolr.Solr('http://177.70.97.79:8983/solr/sptrans', timeout=10)
import json
from TweetSolrDocument import TweetSolrDocument
import codecs
from tweepy import OAuthHandler
import tweepy
from collections import namedtuple
import time
distritos = None

def getReach(twitterID, api):
        try:
            reach = 0
            result = api.retweeters(id=twitterID, count=1000)
            if len(result) > 0 :
                retweet_users = api.lookup_users(result)
                count = 1
                total = len(result)
                for u in retweet_users:
                    print (u.name + ":" +str(count) + "/" +  str(total))
                    count += 1
                    reach += u.followers_count

            print (reach);
            return reach;
        except:
            return -1






def main():
    json_config=codecs.open('config.json',"r", "utf-8")
    # transforma json em objeto python
    config = json.loads(json_config.read(), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    json_config.close();
    auth = OAuthHandler(config.twitter.consumer_key, config.twitter.consumer_secret)
    auth.set_access_token(config.twitter.access_token, config.twitter.access_token_secret)
    api = tweepy.API(auth)
    tweets = db.tweets.find()
    for t in tweets:
        #ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(t['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))

        solrDoc = TweetSolrDocument(t, True)
        solrDoc.reach = solrDoc.user_followers_count
        print (solrDoc.raw_text.encode('utf8'))
        #solrDoc.reach += getReach(solrDoc.id, api);
        solr.add([{
                "id":solrDoc.id,
                "hashtags":solrDoc.hashtags,
                "reply_to_user_id":solrDoc.reply_to_user_id,
                "reply_to_screen_name":solrDoc.reply_to_screen_name,
                "reply_to_status_id":solrDoc.reply_to_status_id,
                "location":solrDoc.location,
                "latitude":solrDoc.location_0_coordinate,
                "longitude":solrDoc.location_1_coordinate,
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
                "filters": config.twitter.filters.split(','),
                "twitter_text": solrDoc.raw_text,
                "pre_process_text":solrDoc.text,
                "reach":solrDoc.reach,
                "sentiment":solrDoc.sentiment,
                "cd_geocodd":solrDoc.cd_geocodd
            }])

    print "FIM"
if __name__ == '__main__':
    main()
