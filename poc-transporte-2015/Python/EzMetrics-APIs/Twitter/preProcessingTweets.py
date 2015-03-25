#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      llima
#
# Created:     08/12/2014
# Copyright:   (c) llima 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import re
import codecs

mycompile = lambda pat:  re.compile(pat,  re.UNICODE)
#SMILEY = mycompile(r'[:=].{0,1}[\)dpD]')
#MULTITOK_SMILEY = mycompile(r' : [\)dp]')

NormalEyes = r'[:=]'
Wink = r'[;]'

NoseArea = r'(|o|O|-)'   ## rather tight precision, \S might be reasonable...

HappyMouths = r'[D\)\]]'
SadMouths = r'[\(\[]'
Tongue = r'[pP]'
OtherMouths = r'[doO/\\]'  # remove forward slash if http://'s aren't cleaned

Happy_RE =  mycompile( '(\^_\^|' + NormalEyes + NoseArea + HappyMouths + ')')
Sad_RE = mycompile(NormalEyes + NoseArea + SadMouths)

Wink_RE = mycompile(Wink + NoseArea + HappyMouths)
Tongue_RE = mycompile(NormalEyes + NoseArea + Tongue)
Other_RE = mycompile( '('+NormalEyes+'|'+Wink+')'  + NoseArea + OtherMouths )

Emoticon = (
    "("+NormalEyes+"|"+Wink+")" +
    NoseArea +
    "("+Tongue+"|"+OtherMouths+"|"+SadMouths+"|"+HappyMouths+")"
)
Emoticon_RE = mycompile(Emoticon)

#Emoticon_RE = "|".join([Happy_RE,Sad_RE,Wink_RE,Tongue_RE,Other_RE])
#Emoticon_RE = mycompile(Emoticon_RE)


def parseEmoticons(text):
    # more complex & harder, so disabled for now
    try:
        h= Happy_RE.search(text)
        s= Sad_RE.search(text)
        w= Wink_RE.search(text)
        t= Tongue_RE.search(text)
        a= Other_RE.search(text)
        h,w,s,t,a = [bool(x) for x in [h,w,s,t,a]]
        if sum([h,w,s,t,a])>1: return text +  " MULTIPLE_EMOTICON"
        if sum([h,w,s,t,a])==1:
            if h: return text +  " HAPPY_EMOTICON"
            if s: return text +  " SAD_EMOTICON"
            if w: return text +  " WINK_EMOTICON"
            if a: return text +  " OTHER_EMOTICON"
            if t: return text +  " TONGUE_EMOTICON"
        return text
    except:
        print "emoticon error"
def getUrls(text):
    try:
        return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    except:
        return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text.decode("utf8"))

def getHashtags(text):
    try:
        return re.findall(r'(?i)\#\w+', text.decode('utf8')) # will includes #
    except:
        return re.findall(r'(?i)\#\w+', text) # will includes #
def getUsers(text):
    try:
        return re.findall(r'(?i)\@\w+', text.decode('utf8')) # will includes #
    except:
        return re.findall(r'(?i)\@\w+', text) # will includes #
def getNumbers(text):
    try:
        return re.findall(r'\d+',text.decode("utf8"));
    except:
        return re.findall(r'\d+',text);

def tweet_pre_process_with__text(text):
    #substituindo hashtags pela tag HT
    hashes = getHashtags(text)
    if hashes !=  None:
        for hash in hashes:
            text = text.replace(hash, hash[1:])
    #subsituindo URLS encontradas pela tag URL

    urls= getUrls(text);
    if urls !=None:
        for url in urls:
            text = text.replace(url, 'URL')
    #substituindo usuários pela tag USR
    users = getUsers(text)
    if users != None:
        for user in users:
            text = text.replace(user, 'USR')

    #substituido qualquer numero por NUM
    numbers = getNumbers(text)
    if len(numbers) > 0:
        if len(numbers) > 1:
            numbers.sort(key = lambda s: len(s))
            numbers = reversed(sorted(numbers, key=len))
        for num in numbers:
            text = text.replace(num, 'NUM')

    return parseEmoticons(text)
def tweet_pre_process_with__tweet_stream(t):
    #substituindo hashtags pela tag HT
    text = t['text']
    for hash in t['entities']['hashtags']:
            text = text.replace(hash['text'], 'HT')
    #subsituindo URLS encontradas pela tag URL
    for url in t['entities']['urls']:
            text = text.replace(url['url'], 'URL')
    #substituindo usuários pela tag USR
    for user in t['entities']['user_mentions']:
            text = replace(user["screen_name"], 'USR')
    return text

def main():
    tweets = codecs.open("tweets/tweets_coletados.txt", "r", "utf-8")
    pre_tweets = codecs.open("tweets/pre_tweets_coletados.txt", "w", "utf-8")
    lines = tweets.readlines()
    for l in lines:
        values = l.split('\t')
        text = values[0];
        preprocess = tweet_pre_process_with__text(text)
        try:
            pre_tweets.write(preprocess + "\t" + values[1] + "\t" + values[2])
        except:
            print 'error'
    pre_tweets.close();
    tweets.close()

if __name__ == '__main__':
    main()
