# -*- coding: utf-8 -*-
import re, string, timeit


exclude = set(string.punctuation)
table = string.maketrans("","")
regex = re.compile('[%s]' % re.escape(string.punctuation))

import sys
import json
import nltk
from Aelius import Toqueniza
import numpy
import urllib2
from BeautifulSoup import BeautifulStoneSoup
import string

#URL = sys.argv[1]
#method = sys.argv[2]
URL = "http://www1.folha.uol.com.br/poder/2015/02/1588416-camara-acelera-projeto-que-trava-fusao-de-partidos.shtml"
method = "mean_score"

# Alguns parâmetros podem ser utilizados para ajustar e melhorar a preformance do algoritmo

N = 100  # Número de palavras a considerar
CLUSTER_THRESHOLD = 5  # Distância entre as palavras a considerar
TOP_SENTENCES = 5  # Número de sentenças para retornar o "top n" summary

# Aborada adptada de  "The Automatic Creation of Literature Abstracts" by H.P. Luhn -- Esse é o cara!

def _score_sentences(sentences, important_words):
    scores = []
    sentence_idx = -1

    for s in [nltk.tokenize.word_tokenize(s) for s in sentences]:

        sentence_idx += 1
        word_idx = []

        # para cada palavra na lista de palavras:
        for w in important_words:
            try:
                # Compute an index for where any important words occur in the sentence

                word_idx.append(s.index(w))
            except ValueError, e: # w not in this particular sentence
                pass

        word_idx.sort()

        # It is possible that some sentences may not contain any important words at all
        if len(word_idx)== 0: continue

        # Using the word index, compute clusters by using a max distance threshold
        # for any two consecutive words

        clusters = []
        cluster = [word_idx[0]]
        i = 1
        while i < len(word_idx):
            if word_idx[i] - word_idx[i - 1] < CLUSTER_THRESHOLD:
                cluster.append(word_idx[i])
            else:
                clusters.append(cluster[:])
                cluster = [word_idx[i]]
            i += 1
        clusters.append(cluster)

        # Score each cluster. The max score for any given cluster is the score
        # for the sentence

        max_cluster_score = 0
        for c in clusters:
            significant_words_in_cluster = len(c)
            total_words_in_cluster = c[-1] - c[0] + 1
            score = 1.0 * significant_words_in_cluster \
                * significant_words_in_cluster / total_words_in_cluster

            if score > max_cluster_score:
                max_cluster_score = score

        scores.append((sentence_idx, score))

    return scores
def removePonctuationInWord(s):
    return s.encode("utf-8").translate(table, string.punctuation)

def removePonctuation(words):
    sword = set(words)
    exclude = set(string.punctuation)
    list=[]
    for w in sword:
        ww= removePonctuationInWord(w)
        if len(ww) >= 3:
            list.append(ww)

    return list

    return list
def summarize(txt, method="mean_score"):
    #t=txt.decode("utf-8")
    sentences = [s for s in Toqueniza.PUNKT.tokenize(txt)]
    normalized_sentences = [s.lower() for s in sentences]

    words = [w.lower() for sentence in normalized_sentences for w in
             Toqueniza.TOK_PORT.tokenize(sentence)]
    words = removePonctuation(words)
    fdist = nltk.FreqDist(words)

    top_n_words = [w[0] for w in fdist.items()
            if w[0] not in nltk.corpus.stopwords.words('portuguese')][:N]
    scored_sentences = _score_sentences(normalized_sentences, top_n_words)


    if method=="mean_score":
        # Summaization Approach 1:
        # Filter out non-significant sentences by using the average score plus a
        # fraction of the std dev as a filter

        avg = numpy.mean([s[1] for s in scored_sentences])
        std = numpy.std([s[1] for s in scored_sentences])
        mean_scored = [(sent_idx, score) for (sent_idx, score) in scored_sentences
                       if score > avg + 0.5 * std]
        return dict(mean_score=[sentences[idx] for (idx, score) in mean_scored])
    elif method == "top_n":

        # Summarization Approach 2:
        # Another approach would be to return only the top N ranked sentences

        top_n_scored = sorted(scored_sentences, key=lambda s: s[1])[-TOP_SENTENCES:]
        top_n_scored = sorted(top_n_scored, key=lambda s: s[0])
        return dict(top_n=[sentences[idx] for (idx, score) in top_n_scored])






# A minimalist approach or scraping the text out of a web page. Lots of time could
# be spent here trying to extract the core content, detecting headers, footers, margins,
# navigation, etc.

def clean_html(html):
    return BeautifulStoneSoup(nltk.clean_html(html),
                              convertEntities=BeautifulStoneSoup.HTML_ENTITIES).contents[0]

if __name__ == '__main__':
    page = urllib2.urlopen(URL).read()

    # It's entirely possible that this "clean page" will be a big mess. YMMV.
    # The good news is that summarize algorithm inherently accounts for handling
    # a lot of this noise.

    clean_page = clean_html(page)

    summary = summarize(clean_page, method)

    print " ".join(summary[method])

