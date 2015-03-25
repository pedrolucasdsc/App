#-------------------------------------------------------------------------------
# Name:        RSSExtractor
# Purpose:
#
# Author:      llima
#
# Created:     16/01/2015
# Copyright:   (c) llima 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sys, codecs
import pika
sys.path.append("G:\\Poc-Transporte\\svn\\Poc-Transporte-2015\\Python\\Utilities")
from TopicHandler import TopicHandler
from future_thread import Future
import json
from collections import namedtuple
import feedparser

import sched, time

config = None
s = sched.scheduler(time.time, time.sleep)


def getRss(channel, ids, config):
    print "getting RSS"
    def checkIds(entry):
        if entry['link'] not in ids:
            if 'updated_parsed' in entry:
                ids[entry['link']] = entry['updated_parsed']
            else:
                ids[entry['link']] = entry['published_parsed']
            return "not exist"
        else:
            if 'updated_parsed' in entry:
                if ids[entry['link']] == entry['updated_parsed']:
                    return "exist"
                else:
                    ids[entry['link']] = entry['updated_parsed']
                    return "update"
            else:
                if ids[entry['link']] == entry['published_parsed']:
                    return "exist"
                else:
                    ids[entry['link']] = entry['published_parsed']
                    return "update"
    hit_list =[]
    for obj in config.rss:
        hit_list.append(obj.url) # list of feeds to pull down

    # pull down all feeds
    future_calls = [Future(feedparser.parse,rss_url) for rss_url in hit_list]
    # block until they are all in
    feeds =[]
    for future_obj in future_calls:
        feeds.append(future_obj())
    entries = []

    for feed in feeds:
        entries.extend( feed[ "items" ] )
    sorted_entries = sorted(entries, key=lambda entry: entry["published_parsed"])
    sorted_entries.reverse() # for most recent entries first

    # jogue todos os items na fila do coelho
    try:

        for entry in sorted_entries:
            check = checkIds(entry)
            if check == "update":
                entry['update'] = True
            #elif check == "not exist" or check == "update":
                #print entry
            print "enviando para a fila: " + entry["link"]
            if 'published' in entry:
                entry['published'] = time.strftime("%d/%m/%Y %H:%M:%S", entry['published_parsed'])
            if 'updated' in entry:
                entry['updated'] = time.strftime("%d/%m/%Y %H:%M:%S", entry['updated_parsed'])
            entry.pop("published_parsed", None)
            entry.pop("updated_parsed", None)

            channel.basic_publish(exchange='',routing_key=config.rabbit.queue,body=json.dumps(entry))
            #else:
                #print "RSS existe:" +  entry["link"]
    except Exception as e:
        print e
    print "waiting 5 minutes."
    s.enter(60*5, 1, lambda: getRss(channel, ids, config), ())



def main():
    json_config=codecs.open("RSSConfig.json","r", "utf8")
    config = json.loads(json_config.read(), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    json_config.close();
    rabbit = pika.BlockingConnection(pika.ConnectionParameters(config.rabbit.server))
    channel = rabbit.channel()
    channel.queue_declare(queue=config.rabbit.queue, durable=True)
    ids = {}
    s.enter(1, 1, lambda: getRss(channel, ids, config), ())
    s.run()


if __name__ == '__main__':
    main()

