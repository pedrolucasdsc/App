﻿#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      llima
#
# Created:     20/02/2015
# Copyright:   (c) llima 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from getSolrQuery import getSolrQuery
from constants import pt_stopwords 
import pysolr
import gensim
from gensim import corpora
from gensim import matutils
from Aelius import Toqueniza
import numpy as np
import networkx as nx
import json, os, sys
import redis

g = nx.DiGraph()
idx = 0
threshold_freq = 1
r_server = None

class CreateNetworkOfTermsGraph:

    def getTweetsByTopics(self, topics):
        solr = pysolr.Solr('http://177.70.97.79:8983/solr/sptrans', timeout=10)
        docs = []
        register_per_page = 100
        for t in topics:
            query = 'pre_process_text:*'+t+'*'
            docs.extend(getSolrQuery(solr, query, register_per_page))
        return docs

    def getTextsByTweets(self, docs):
        texts = []
        for d in docs:
            texts.append(d['pre_process_text'])
        return texts

    def createVocabulary(self, documents, path_vocab, topics):
        pt_stopwords.extend(topics)
        pt_stopwords.extend(["onibus", u"ônibus","...","..","!","@","#","$","%","&","*","(",")","-","+","_","=","\"","\'","~","^","´","`","{","}","[","]","\\","/","?",";",":",".",",","<",">","|","rt","usr","url", "num", "happy_emoticon", "sad_emoticon", "wink_emoticon", "other_emoticon", "tongue_emoticon", "multiple_emoticon"]);
        stoplist = set(pt_stopwords)
        # remove as stopwords
        texts = [[word for word in Toqueniza.TOK_PORT.tokenize(document.lower()) if word not in stoplist]
                 for document in documents]

        # remove palavras que aparecem uma única vez
        all_tokens = sum(texts, [])
        tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
        texts = [[word for word in text if word not in tokens_once]
                for text in texts]
        # extraindo o vocabulario
        dictionary = corpora.Dictionary(texts)

        # salvando o vocabulario
        dictionary.save(path_vocab) # store the dictionary, for future reference
        return [dictionary,texts]

    def createNodeAndEdges(self, row):
        global g
        global idx
        idx2 = 0
        for value in row:
             if idx2 == idx or value <= threshold_freq: # só adiciona uma aresta se o valor for >= 10 ou se o indice forem diferentes
                idx2 += 1
                continue
             g.add_edge(idx, idx2, {'freq': str(value)})
             g.node[idx] = {"freq": str(row[idx])}
             g.node[idx2] = {"freq": str(row[idx2])}
             idx2 += 1
        #if row[idx] < 100:

        idx += 1
    def createWordGraph(self, matrix):
        for row in matrix:
            self.createNodeAndEdges(row)


    def write_d3js_output(self, g, dictionary, out_file, topics):
        nodes = g.nodes()
        indexed_nodes = {}
        idx = 0
        for n in nodes:
            indexed_nodes.update([(n, idx,)])
            idx += 1
            links = []
        groups = {}
        for n1, n2 in g.edges():
            if groups.has_key(indexed_nodes[n1]):
                groups[indexed_nodes[n1]].append(indexed_nodes[n2])
            else:
                groups[indexed_nodes[n1]] = [indexed_nodes[n1], indexed_nodes[n2]]
            links.append({'source' : indexed_nodes[n2],
                        'target' : indexed_nodes[n1],
                        'value': g.edge[n2][n1]['freq']})

        # merging groups

        jsond = {"nodes":[], "links":links};


        finalgroups = groups

        idx = 0
        for n in nodes:
            for k in finalgroups.keys():
                if idx in finalgroups[k]:
                    try:
                        img = g.node[n]["freq"]
                    except:
                        print n

                    no = {"freq":img, "nodeName": dictionary[n], "group": k}
                    jsond["nodes"].append(no)
                    break
            idx += 1
        json_data = json.dumps(jsond, indent=4)
        if not os.path.isdir('out'):
            os.mkdir('out')
        f = open(out_file, 'w')
        f.write(json_data)
        f.close()
        #save to redis
        self.save_to_redis("_".join(topics), json_data)
        print >> sys.stderr, 'Data file written to: %s' % f.name
        
    def save_to_redis(self, chave, valor):
        try:
            global r_server
            r_server.sadd(chave, valor)
            return true
        except:
            return False

    def __init__(self, topics, ipRedis):
        try:
            global r_server
            r_server = redis.Redis(host=ipRedis)
            
            #topics = ['HAPPY_EMOTICON']
            docs = self.getTweetsByTopics(topics)
            documents = self.getTextsByTweets(docs)
            retorno = self.createVocabulary(documents, 'out/sptrans_tweets.dict', topics)
            dictionary = retorno[0]
            texts = retorno[1]
            print(dictionary)
            # criando o corpus bag of words
            corpus = [dictionary.doc2bow(text) for text in texts]
            corpora.MmCorpus.serialize('out/sptrans_tweets.mm', corpus) # store to disk, for later use
            num_terms = len(dictionary)
            # gerando a matriz de termos x documentos
            terms_documents = matutils.corpus2dense(corpus, num_terms)
            # gerando a matriz de co-ocorrencia de palavras
            word_cooccur =  np.dot(terms_documents, terms_documents.transpose())
            self.createWordGraph(word_cooccur)
            self.write_d3js_output(g, dictionary, 'out/sptrans_tweets_word_matrix.json', topics)
            #scipy_csc_matrix = matutils.corpus2csc(corpus)
            
            print "Success"
        except:
            print "Error"
