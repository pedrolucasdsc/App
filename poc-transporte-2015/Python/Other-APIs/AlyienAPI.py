#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      llima
#
# Created:     20/01/2015
# Copyright:   (c) llima 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from bottle import route, run, request, abort, hook, response

from aylienapiclient import textapi

AppID = "9b429c83" # Ezute Application
AppKey = "11fb7c535d583a0b778839acaed42259"

def encoded_dict(in_dict):
    out_dict = {}
    for k, v in in_dict.iteritems():
        if isinstance(v, unicode):
            v = v.encode('utf8')
        elif isinstance(v, str):
            # Must be encoded in UTF-8
            v.decode('utf8')
        out_dict[k] = v
    return out_dict

@hook('after_request')
def enable_cors():
    print('enable cors')
    response.headers['Access-Control-Allow-Origin'] = '*'

@route('/Aylien/sentiment', method='POST')
def getSentiment():
    c = textapi.Client(AppID, AppKey)
    s = c.Sentiment(request.json)
    return s;

@route('/Aylien/articleExtraction', method='POST')
def getArticleExtraction():
    c = textapi.Client(AppID, AppKey)
    a = c.Extract(request.json)
    return a

@route('/Aylien/classify', method='POST') #Classifies a piece of text according to IPTC NewsCode standard.
def getClassification():
    #parameters: url or text, language(optional):Valid options are: "en", "de", "fr", "es", "it", "pt", and "auto".
    c = textapi.Client(AppID, AppKey)
    a = c.Classify(encoded_dict(request.json))
    return a

@route('/Aylien/conceptExtraction', method='POST') #Extracts named entities mentioned in a document, disambiguates and cross-links them to DBPedia and Linked Data entities, along with their semantic types (including DBPedia and schema.org).
def getClassification():
    #parameters: url, text, language(optional):Valid options are: "en", "de", "fr", "es", "it", "pt", and "auto".
    c = textapi.Client(AppID, AppKey)
    a = c.Concepts(encoded_dict(request.json))
    return a

@route('/Aylien/summarize', method='POST') #Summarizes an article into a few key sentences.
def getSummarization():
    #parameters: url, text, language(optional):Valid options are: "en", "de", "fr", "es", "it", "pt", and "auto".
    """
    'mode (str, optional)': Analyze mode. Valid options are default
          and short. Default is default. short mode produces shorter
          sentences.
        'text (str, optional)': Text,
        'title (str, optional)': Title,
        'url (str, optional)': URL,
        'sentences_number': Number of sentences to be returned.
          Only in default mode (not applicable to short mode).
          Default value is 5.
          has precedence over sentences_percentage.
        'sentences_percentage': Percentage of sentences to be returned.
          Only in default mode (not applicable to short mode).
          Possible range is 1-100.
          sentences_number has precedence over this parameter.
    """
    c = textapi.Client(AppID, AppKey)
    a = c.Summarize(encoded_dict(request.json))
    return a


def main():
    run(host='localhost', port=8081)

if __name__ == '__main__':
    main()
