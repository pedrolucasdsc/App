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
from collections import namedtuple
import codecs
import json
import sys
json_config=codecs.open("TwitterConfig.json","r", "utf8")
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

from bottle import route, run, request
import unirest
from pprint import pprint
from CreateFriendshipGraph import CreateFriendshipGraph
from CreateNetworkOfTermsGraph import CreateNetworkOfTermsGraph
from CreateRetweetsRelationshipsGraph import CreateRetweetsRelationshipsGraph
from GetFriendsFollowersInfo import GetFriendsFollowersInfo
from Crawl import Crawl
import twitter

token = config.twitter.token
token_secret = config.twitter.token_secret
con_key = config.twitter.con_key
con_secret = config.twitter.con_secret
auth=twitter.OAuth(token, token_secret, con_key, con_secret)
t = twitter.Twitter(domain='api.twitter.com', auth=auth, api_version='1.1')

@route('/Graph/CreateRetweetsRelationships', method='POST')
def CreateRetweetsRelationships():
    try:
        global config
        word = request.forms.get('word')
        CreateRetweetsRelationshipsGraph(word, config.serverSolrIp, config.serverRedisIp)
        jsonRetorno = '{"status":"success","descricao":"Documento salvo"}'
    except Exception as e:
        pprint(e)
        jsonRetorno = '{"status":"failed","descricao":'+json.dumps(e)+'}'
    return jsonRetorno

@route('/Graph/CreateNetworkOfTerms', method='POST')
def CreateNetworkOfTerms():
    try:
        global config
        topics = request.forms.get('topics')
        arrayTopics = topics.strip().split(',')
        CreateNetworkOfTermsGraph(arrayTopics, config.serverRedisIp)
        jsonRetorno = '{"status":"success","descricao":"Documento salvo"}'
    except Exception as e:
        pprint(e)
        jsonRetorno = '{"status":"failed","descricao":'+json.dumps(e)+'}'
    return jsonRetorno

@route('/Graph/CreateFriendShip', method='POST')
def CreateFriendShipGraph():
    try:
        screenName = request.forms.get('screen_name')
        CreateFriendshipGraph(screenName)
        jsonRetorno = '{"status":"success","descricao":"Documento salvo"}'
    except Exception as e:
        pprint(e)
        jsonRetorno = '{"status":"failed","descricao":'+json.dumps(e)+'}'
    return jsonRetorno

@route('/User/Info/:id', method='GET')
def GetUserInfo(id):
    try:
        objGetFriendsFollowersInfo = GetFriendsFollowersInfo(t)
        jsonRetorno = objGetFriendsFollowersInfo.get_info_by_id([id])
    except Exception as e:
        pprint(e)
        jsonRetorno = '{"status":"failed","descricao":'+json.dumps(e)+'}'
    return jsonRetorno

@route('/User/Friends/:id', method='GET')
def GetUserFriends(id):
    try:
        objCrawl = Crawl(config.serverRedisIp, t)
        jsonRetorno = objCrawl.get_all_friends_ids(id)
    except Exception as e:
        pprint(e)
        jsonRetorno = '{"status":"failed","descricao":'+json.dumps(e)+'}'
    return {"friends_ids":jsonRetorno}

@route('/User/Followers/:id', method='GET')
def GetUserFollowers(id):
    try:
        objCrawl = Crawl(config.serverRedisIp, t)
        jsonRetorno = objCrawl.get_all_followers_ids(id)
    except Exception as e:
        pprint(e)
        jsonRetorno = '{"status":"failed","descricao":'+json.dumps(e)+'}'
    return {"friends_ids":jsonRetorno}

run(host='10.10.4.27', port=8083)


