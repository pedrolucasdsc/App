#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      llima
#
# Created:     24/11/2014
# Copyright:   (c) llima 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from Aelius import AnotaCorpus, Toqueniza, Extras, Chunking

def parseTreeToFlareJson(tree):
    json = {"name": tree.node, "children":[]}
    height = tree.height();
    for el in tree.leaves():
        pass

def main():
    sent=AnotaCorpus.EXEMPLO
    tokens=Toqueniza.TOK_PORT.tokenize(sent)
    lx=Extras.carrega("lxtagger")
    m=AnotaCorpus.HUNPOS


    tokens = [u'Na', u'Europa', u'e', u'nos', u'Estados', u'Unidos', u',', u'a', u'\xe1rea', u'da', u'Lingu\xedstica', u'Computacional', u'est\xe1', u'em', u'extrema', u'expans\xe3o', u'e', u'goza', u'de', u'muita', u'popularidade', u',', u'tanto', u'nos', u'cursos', u'de', u'Ci\xeancias', u'da', u'Computa\xe7\xe3o', u'quanto', u'nos', u'de', u'Lingu\xedstica', u'.']
    #anotadas=AnotaCorpus.anota_sentencas([tokens],lx,"mxpost",separacao_contracoes=True)
    anotadas=AnotaCorpus.anota_sentencas([tokens],m, arquitetura='hunpos', separacao_contracoes=True)
    #for w,t in anotadas[0]:
    #    print "%s/%s " % (w,t),

    print "\n"
    #Em/PREP  a/DA  Europa/PNM  e/CJ  em/PREP  os/DA  Estados/PNM  Unidos/PNM  ,/PNT  a/DA  área/CN  de/PREP  a/DA  Linguística/PNM  Computacional/PNM  está/V  em/PREP  extrema/ADJ  expansão/CN  e/CJ  goza/CN  de/PREP  muita/QNT  popularidade/CN  ,/PNT  tanto/ADV  em/PREP  os/DA  cursos/CN  de/PREP  Ciências/PNM  de/PREP  a/DA  Computação/CN  quanto/REL  nos/CL  de/PREP  Linguística/PNM  ./PNT
    #Em/P  a/D-F  Europa/NPR  e/CONJ  em/P  os/D-P  Estados/NPR-P  Unidos/NPR-P  ,/,  a/D-F  área/ADJ-F  de/P  a/D-F  Linguística/ADJ-F  Computacional/NPR  está/ET-P  em/P  extrema/ADJ-F  expansão/N  e/CONJ  goza/VB-P  de/P  muita/Q-F  popularidade/N  ,/,  tanto/ADV-R  em/P  os/D-P  cursos/N-P  de/P  Ciências/NPR-P  de/P  a/D-F  Computação/N  quanto/WADV  nos/CL  de/P  Linguística/NPR  ./.
    an = [("Em","PREP"),("a","DA"),("Europa","PNM"),("e","CJ"),("em","PREP"),("os","DA"),("Estados","PNM"),("Unidos","PNM"),(",","PNT"),("a","DA"),("área","CN"),("de","PREP"),("a","DA"),("Linguística","PNM"),("Computacional","PNM"),("está","V"),("em","PREP"),("extrema","ADJ"),("expansão","CN"),("e","CJ"),("goza","CN"),("de","PREP"),("muita","QNT"),("popularidade","CN"),(",","PNT"),("tanto","ADV"),("em","PREP"),("os","DA"),("cursos","CN"),("de","PREP"),("Ciências","PNM"),("de","PREP"),("a","DA"),("Computação","CN"),("quanto","REL"),("nos","CL"),("de","PREP"),("Linguística","PNM"),(".","PNT")]

    chunks=Chunking.CHUNKER.batch_parse([an])
    tree = chunks[0]
    tree.draw();
    print(chunks[0].pprint())

if __name__ == '__main__':
    main()
