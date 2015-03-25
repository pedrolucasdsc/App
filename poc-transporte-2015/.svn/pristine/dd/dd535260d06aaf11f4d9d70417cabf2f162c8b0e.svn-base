import pytz
import sys
from datetime import datetime, timedelta
from email.utils import parsedate_tz
from pymongo import Connection
from preProcessingTweets import tweet_pre_process_with__text
import unirest
import pysolr
import pymongo
import json
import re
from bs4 import BeautifulSoup
local_tz = pytz.timezone('America/Sao_Paulo')
unirest.timeout(3600)
config = None

def getDateExtensions(datestring):
    #"2014-01-02T06:54:36Z" Exemplo de data para o parse
    values = datestring.split('T')
    dateValues = values[0].split('-')
    timeValues = values[1].split(':')
    dtExtension = {

        "DT_YEAR": dateValues[0],
        "DT_MONTH": dateValues[1],
        "DT_YEAR_MONTH": dateValues[0]+"-"+dateValues[1],
        "DT_DAY": dateValues[2],
        "DT_YEAR_MONTH_DAY": values[0],
        "DT_HOUR": timeValues[0],
        "DT_YEAR_MONTH_DAY_HOUR": values[0] + " " +  timeValues[0]+":00:000"
    }
    return dtExtension

def to_datetime(datestring):
    time_tuple = parsedate_tz(datestring.strip())
    dt = datetime(*time_tuple[:6])
    return dt - timedelta(seconds=time_tuple[-1])

def tweet_pre_process(t):
    return tweet_pre_process_with__text(t['text'])

def ExtractorElementWebPage(jsonFind):
    global config
    return unirest.post("http://" + config.ExtractorElementWebPageApi.server + ":" + config.ExtractorElementWebPageApi.port + "/" + config.ExtractorElementWebPageApi.title,
        headers = { "Accept" : "application/json", "Content-Type": "application/json"},
        params = json.dumps(jsonFind)
    )


def getJsonFaceRecognition(urlImage):
    global config
    return unirest.post("http://" + config.faceRecognitionApi.server + ":" + config.faceRecognitionApi.port + "/" + config.faceRecognitionApi.title, headers = { "Accept" : "application/json" }, params = {"api_key": config.faceRecognitionApi.api_key, "api_secret": config.faceRecognitionApi.api_secret, "linkImg": urlImage})

def getDistrictCode():
    return {}
    connection = Connection(config.mongodbSpatial.server)
    db = connection[config.mongodbSpatial.database]

def getSentiment(text):
    global config
    return unirest.post("http://" + config.sentimentAnalysisApi.server + ":" + config.sentimentAnalysisApi.port + "/" + config.sentimentAnalysisApi.title,
    headers = { "Accept" : "application/json", "Content-Type": "application/json"},
    params = json.dumps({"text" : text}))

def getSource(source):
    try:
        soup = BeautifulSoup(source)
        source_text = soup.find('a').contents[0]
    except:
        print('error in getSource')
        source_text = "error"
    return source_text
def getExpandedUrl(url):
    ret = unirest.get("http://api.longurl.org/v2/expand?url="+url+ "&format=json")
    if "long-url" in ret.body:
        return ret.body['long-url']
    else:
        return ""
class TweetSolrDocument():
    def __init__(self, t, arqConfig):
        global config
        config = arqConfig

        self.id = t['id'] # twitter_id
        self.hashtags =[]
        self.urls =[]
        self.domains = []
        for url in t['entities']['urls']:
            expanded_url = getExpandedUrl(url['expanded_url'])
            self.urls.append(pysolr.force_bytes(expanded_url))
            domain = re.findall(".*\://(?:www.)?([^\/]+)", expanded_url)

            if len(domain) >0:
                self.domains.append(pysolr.force_bytes(domain[0]))
        for hash in t['entities']['hashtags']:
            self.hashtags.append(pysolr.force_bytes(hash['text']))
        self.reply_to_user_id = t['in_reply_to_user_id']
        self.reply_to_screen_name= pysolr.force_bytes(t['in_reply_to_screen_name'])
        self.reply_to_status_id= t['in_reply_to_status_id']
        self.location = []
        self.latitude = None
        self.longitude = None
        self.geocodd = -1
        print "#################################"
        print t['coordinates']
        print "#################################"
        if t['coordinates'] != None:
            self.location= [str(t['coordinates']['coordinates'][1]) ,  str(t['coordinates']['coordinates'][0])]
            self.latitude = t['coordinates']['coordinates'][0]
            self.longitude = t['coordinates']['coordinates'][1]
            #self.geocodd = getGeoCodd(self.latitude, self.longitude)
        self.city = pysolr.force_bytes(t['user']['location'])
        self.number_of_retweets= t['retweet_count']
        self.source= pysolr.force_bytes(t['source'])
        self.raw_text = pysolr.force_bytes(t['text'])
        self.text=pysolr.force_bytes(tweet_pre_process(t))
        self.sender_user_id= t['user']['id']
        self.sender_screen_name= pysolr.force_bytes(t['user']['screen_name'])
        self.sender_name= pysolr.force_bytes(t['user']['name'])
        self.is_favorited= t['favorited']
        self.is_retweet= t['retweeted']
        self.url_user_image = pysolr.force_bytes(t['user']['profile_image_url'])
        self.user_followers_count = t['user']['followers_count'] #The number of followers the author of a Tweet has on Twitter.
        self.user_statuses_count = t['user']['statuses_count'] #The total number of Tweets and Retweets a Twitter user has posted.
        self.user_listed_count = t['user']['listed_count'] #The number of Twitter lists on which the author of a Tweet appears.
        self.url_entities_list=[]
        self.user_mention_list = []
        self.user_mention_screen_name= []
        for user in t['entities']['user_mentions']:
            self.user_mention_list.append(user["id"])
            self.user_mention_screen_name.append(pysolr.force_bytes(user["screen_name"]))
        self.creation_date= to_datetime(t['created_at']).strftime ("%Y-%m-%dT%H:%M:%SZ")
        dtValues = getDateExtensions(self.creation_date)

        self.creation_date_YEAR =dtValues["DT_YEAR"];
        self.creation_date_MONTH =dtValues["DT_MONTH"];
        self.creation_date_YEAR_MONTH =dtValues["DT_YEAR_MONTH"];
        self.creation_date_DAY =dtValues["DT_DAY"];
        self.creation_date_YEAR_MONTH_DAY=dtValues["DT_YEAR_MONTH_DAY"];
        self.creation_date_HOUR =dtValues["DT_HOUR"];
        self.creation_date_YEAR_MONTH_DAY_HOUR =dtValues["DT_YEAR_MONTH_DAY_HOUR"];

        self.filters = pysolr.force_bytes(t['filters'])

        #ValoreSimuloados
        self.reach = -1
        #sentimentResponse = getSentiment(self.raw_text).body;
        sentimentResponse = {"status":"nok"}
        if sentimentResponse["status"] == "OK":
            if sentimentResponse["docSentiment"]["type"] == "positive":
                self.sentiment = "positivo"
                self.float_sentiment = float(sentimentResponse["docSentiment"]["score"])
            elif sentimentResponse["docSentiment"]["type"] == "negative":
                self.sentiment = "negativo"
                self.float_sentiment = float(sentimentResponse["docSentiment"]["score"])
            else:
                self.sentiment = "neutro"
                self.float_sentiment = 0.0
        else:
            self.sentiment = "unclassified"
            self.float_sentiment = 0.0

        self.sentimentB =  0.0
        self.sentimentC = 0.0
        self.topico = 'unclassified'
        self.source_text = getSource(self.source)


        #ExtractorUrlImageTwitter
        self.image_face_recognition = ""
        myjson = {"urlWebPage":"https://twitter.com/" + self.sender_screen_name.strip(), "tag":"img", "find":{"class":"ProfileAvatar-image"}};
        print myjson;
        jsonExtractorUrlImageTwitter = ExtractorElementWebPage(myjson).body

        self.image_face_recognition = jsonExtractorUrlImageTwitter['element']

        #FaceRecognition
        self.user_gender = None
        self.user_age = -1
        self.user_age_range = -1
        if self.image_face_recognition != "":
            jsonFaceRecognition = getJsonFaceRecognition(self.image_face_recognition)
            if 'error' not in jsonFaceRecognition.body:
                if len(jsonFaceRecognition.body["face"]) == 1:
                    t['face'] = jsonFaceRecognition.body['face'][0];
                    if 'attribute' in jsonFaceRecognition.body["face"][0]:
                        self.user_gender = jsonFaceRecognition.body['face'][0]['attribute']['gender']['value']
                        self.user_age = int(jsonFaceRecognition.body['face'][0]['attribute']['age']['value'])
                        self.user_age_range = int(jsonFaceRecognition.body['face'][0]['attribute']['age']['range'])



