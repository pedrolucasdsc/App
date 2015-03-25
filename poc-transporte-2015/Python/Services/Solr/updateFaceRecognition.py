'''
Created on 22/01/2015

@author: pcosta
'''

from pymongo import MongoClient
import unirest

def InsereMongo():
    con = MongoClient('177.70.97.184', 27017)
    coll = con.sptrans.tweets
    tweets = coll.find({"face":{"$exists":False}})
    unirest.timeout(3600)
    #jsonFace = unirest.post("http://10.10.4.27:8080/EzMetrics/FaceRecognition", headers = { " Accept " : " application/json " }, params = { "mashape" : "au78YMXLmRmsh9PI0uiKy2oO2akZp1iYp9ajsnIZtlinxJZB5O" , "linkImg" : tweets[0]['user']['profile_image_url_https']})
    #tweets[0]["face"] = jsonFace["face"]
    total = tweets.count()
    c = 0
    for tweet in tweets:
        jsonFace = unirest.post("http://10.10.4.27:8080/EzMetrics/FaceRecognition", headers = { " Accept " : " application/json " }, params = { "mashape" : "au78YMXLmRmsh9PI0uiKy2oO2akZp1iYp9ajsnIZtlinxJZB5O" , "linkImg" : tweet['user']['profile_image_url']})

        if "face" in jsonFace.body:
            print tweet['user']['profile_image_url']
            tweet['face'] = jsonFace.body["face"]
            try:
                print jsonFace.body["face"]
                if "attribute" in jsonFace.body["face"] :
                    print "encontrou"
                else:
                    tweet['face'] = "not found"
                coll.save(tweet)
            except:
                tweet['face'] = "error"
        else:

            tweet['face']={}
            coll.save(tweet)
        c+=1
        print str(c) + "/" + str(total)
    return


if __name__ == '__main__':
    InsereMongo()
    pass
