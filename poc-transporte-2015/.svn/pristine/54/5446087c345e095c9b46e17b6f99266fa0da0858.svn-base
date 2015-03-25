#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""template.py: Description of what the module does."""

from enum import Enum


##Token = Enum(UNKNOWN='<UNK>',
##             SENT_START='<S>',
##             SENT_END='</S>',
##             PAD='<PAD>')
##
##TokenID = Enum(UNKNOWN=0,
##               SENT_START=1,
##               SENT_END=2,
##               PAD=3)

class Token(Enum):
    UNKNOWN='<UNK>'
    SENT_START='<S>'
    SENT_END='</S>'
    PAD='<PAD>'

class TokenID(Enum):
    UNKNOWN=0,
    SENT_START=1
    SENT_END=2
    PAD=3

pt_stopwords = ['p', 'pro','pra','aqui',u'é', 'de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'com',
 'n\xc3\xa3o', 'uma', 'os', 'no', 'se', 'na', 'por', 'mais', 'as', 'dos', 'como',
'mas', 'ao', 'ele', 'das', '\xc3\xa0', 'seu', 'sua', 'ou', 'quando', 'muito',
'nos', 'j\xc3\xa1', 'eu', 'tamb\xc3\xa9m', 's\xc3\xb3', 'pelo', 'pela', 'at\xc3\xa9',
'isso', 'ela', 'entre', 'depois', 'sem', 'mesmo', 'aos', 'seus', 'quem', 'nas', 'me',
'esse', 'eles', 'voc\xc3\xaa', 'essa', 'num', 'nem', 'suas', 'meu', '\xc3\xa0s', 'minha',
 'numa', 'pelos', 'elas', 'qual', 'n\xc3\xb3s', 'lhe', 'deles', 'essas', 'esses', 'pelas',
'este', 'dele', 'tu', 'te', 'voc\xc3\xaas', 'vos', 'lhes', 'meus', 'minhas', 'teu', 'tua',
'teus', 'tuas', 'nosso', 'nossa', 'nossos', 'nossas', 'dela', 'delas', 'esta', 'estes',
'estas', 'aquele', 'aquela', 'aqueles', 'aquelas', 'isto', 'aquilo', 'estou', 'est\xc3\xa1',
 'estamos', 'est\xc3\xa3o', 'estive', 'esteve', 'estivemos', 'estiveram', 'estava',
'est\xc3\xa1vamos', 'estavam', 'estivera', 'estiv\xc3\xa9ramos', 'esteja', 'estejamos',
'estejam', 'estivesse', 'estiv\xc3\xa9ssemos', 'estivessem', 'estiver', 'estivermos',
'estiverem', 'hei', 'h\xc3\xa1', 'havemos', 'h\xc3\xa3o', 'houve', 'houvemos', 'houveram',
'houvera', 'houv\xc3\xa9ramos', 'haja', 'hajamos', 'hajam', 'houvesse', 'houv\xc3\xa9ssemos',
'houvessem', 'houver', 'houvermos', 'houverem', 'houverei', 'houver\xc3\xa1', 'houveremos',
 'houver\xc3\xa3o', 'houveria', 'houver\xc3\xadamos', 'houveriam', 'sou', 'somos', 's\xc3\xa3o',
 'era', '\xc3\xa9ramos', 'eram', 'fui', 'foi', 'fomos', 'foram', 'fora', 'f\xc3\xb4ramos',
'seja', 'sejamos', 'sejam', 'fosse', 'f\xc3\xb4ssemos', 'fossem', 'for', 'formos', 'forem',
'serei', 'ser\xc3\xa1', 'seremos', 'ser\xc3\xa3o', 'seria', 'ser\xc3\xadamos', 'seriam',
'tenho', 'tem', 'temos', 't\xc3\xa9m', 'tinha', 't\xc3\xadnhamos', 'tinham', 'tive', 'teve',
'tivemos', 'tiveram', 'tivera', 'tiv\xc3\xa9ramos', 'tenha', 'tenhamos', 'tenham', 'tivesse',
 'tiv\xc3\xa9ssemos', 'tivessem', 'tiver', 'tivermos', 'tiverem', 'terei', 'ter\xc3\xa1',
'teremos', 'ter\xc3\xa3o', 'teria', 'ter\xc3\xadamos', 'teriam']