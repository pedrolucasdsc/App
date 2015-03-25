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
from Aelius import Toqueniza, Chunking
import re, string, unicodedata, codecs, json
exclude = set(string.punctuation)
table = string.maketrans("","")
regex = re.compile('[%s]' % re.escape(string.punctuation))

# classe que manipula a extração de tópicos em um documento ou feed.
class TopicHandler():
    def __init__(self, arqConfig):
        self.dictSiglas = {}
        self.municipios = self.createMunicipiosFromFile(arqConfig.municipios_file)
        self.palavras_compostas = arqConfig.palavras_compostas
        self.palavras_compostas.extend(self.createPalavrasCompostasDeMunicipios())
        self.topicos = arqConfig.topicos
        self.dictContem = self.createTopicDictionaryContem()
        self.dictObrigatorio = self.createTopicDictionaryObrigatorio()
        self.dictTopicoObrigatorio = self.createDictTopicoObrigatorio()
        self.dictMunicipiosEstados = self.createDictMunicipiosEstados()
        self.dictIgnore = self.createDictIgnore()


    def createPalavrasCompostasDeMunicipios(self):
        palavras_compostas = []
        estados = {}
        for m in self.municipios:
            value = m['nome'].split(' ')
            if len(value) > 1:
                nome = m['nome'].lower()
                palavras_compostas.append(m['nome'].lower())
                nome2 = unicodedata.normalize('NFKD', nome).encode('ascii', 'ignore')
                if nome2 != nome:
                    palavras_compostas.append(nome2.decode('utf-8'))

            value = m['nome_uf'].split(' ')
            if len(value) > 1:
                if not estados.has_key(m['nome_uf'].lower()):
                    estados[m['nome_uf'].lower()] = True
                    nome = m['nome_uf'].lower()
                    palavras_compostas.append(nome)
                    nome2 = unicodedata.normalize('NFKD', nome).encode('ascii', 'ignore')
                    if nome2 != nome:
                        palavras_compostas.append(nome2.decode('utf-8'))
        return palavras_compostas

    def createMunicipiosFromFile(self,path):
        municipios = codecs.open(path,"r", "utf-8");
        txt = municipios.readlines();
        lstMunicipios = []
        for l in txt:
            jsonMunicipios = json.loads(l)
            lstMunicipios.extend(jsonMunicipios['_embedded']['municipios'])
        return lstMunicipios

    def createDictMunicipiosEstados(self):
        dict = {}
        palavras = []
        estados ={}
        siglas = {}
        for m in self.municipios:
            value = m['nome'].split(' ')
            siglas.setdefault(m['sigla_uf'], True)
            if len(value) > 1:
                nome = m['nome'].lower().replace(" ","_")
                palavras.append(nome)
                nome2 = unicodedata.normalize('NFKD', nome).encode('ascii', 'ignore')
                if nome2 != nome:
                    palavras.append(nome2.decode("utf-8"))
            else:
                palavras.append(m['nome'].lower())
            value = m['nome_uf'].split(' ')
            if len(value) > 1:
                if not estados.has_key(m['nome_uf'].lower()):
                    estados[m['nome_uf'].lower()] = True
                    nome = m['nome_uf'].lower().replace(" ","_")
                    print nome
                    palavras.append(m['nome_uf'].lower())
                    nome2 = unicodedata.normalize('NFKD', nome).encode('ascii', 'ignore')
                    if nome2 != nome:
                        palavras.append(nome2.decode("utf-8"))
            else:
                palavras.append(m['nome_uf'].lower())
        for t in self.topicos:
            palavras_topicos = list(palavras)
            siglas_topicos = list(siglas.keys())
            if hasattr(t.content, 'siglas'):
                for s in t.content.siglas:
                    siglas_topicos.remove(s)
                self.dictSiglas[t.topico] = siglas_topicos
            if hasattr(t.content, 'municipios'):
                for m in t.content.municipios:
                    palavras_topicos.remove(m)
                dict[t.topico] = palavras_topicos

        return dict

    def createDictIgnore(self):
        dict = {}
        for t in self.topicos:
            if hasattr(t.content, 'municipios'):
                dict[t.topico] = self.dictMunicipiosEstados[t.topico]
                if hasattr(t.content, 'ignore'):
                    dict[t.topico].extend(t.content.ignore)
            else:
                if hasattr(t.content, 'ignore'):
                    dict[t.topico] = t.content.ignore
                else:
                    dict[t.topico] = []
        return dict

    def createDictTopicoObrigatorio(self):
        dict ={}
        for t in self.topicos:
            if len(t.content.obrigatorio) > 0:
                dict[t.topico] = True
        return dict
    def createTopicDictionaryContem(self):
        dict ={}
        for t in self.topicos:
            for word in t.content.contem:
                if dict.has_key(word):
                    dict[word].append(t.topico)
                else:
                    dict[word] = [t.topico]
        return dict
    def createTopicDictionaryObrigatorio(self):
        dict ={}
        for t in self.topicos:
            dict[t.topico] = []
            for word in t.content.obrigatorio:
                dict[t.topico].append(word)
        return dict

    def f7(self, seq):
        seen = set()
        seen_add = seen.add
        return [ x for x in seq if not (x in seen or seen_add(x))]

    def getWords(self,text):
        # cria as palavras compostas
        #text = re.sub(r'[^\w\s\"\'!@#$%&*(){}[]<>|\n]','',text)
        text = text.encode('utf-8').translate(table, string.punctuation).decode('utf-8')
        for p in self.palavras_compostas:
            try:
                if p.encode("utf8") in text:
                    unique_word = p.replace(" ", "_")
                    text = text.replace(p.encode("utf8"), unique_word.encode("utf8"))
            except:
                if p in text:
                    unique_word = p.replace(" ", "_")
                    text = text.replace(p, unique_word)
        tokens=Toqueniza.TOK_PORT.tokenize(text)
        return tokens
    def getTopicos(self, text):
        topics = []

        words = self.getWords(text)
        found_topic = False
        for w in words:
            if self.dictContem.has_key(w.lower()):
                for c in self.dictContem[w.lower()]:
                    if self.dictTopicoObrigatorio.has_key(c):
                        found_obrigatorio = False

                        palavras_obrigatorias = set(self.dictObrigatorio[c])
                        inter = set.intersection(palavras_obrigatorias, set(words))
                        if len(inter) > 0:
                            topics.append(c)
                    else:
                        topics.append(c)

        topics = self.f7(topics)
        return topics

