#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      llima
#
# Created:     02/12/2014
# Copyright:   (c) llima 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from pygeocoder import Geocoder
import codecs
import json
def main():
    f = codecs.open('G:\\Poc-Transporte\\Dados SPTrans\\terminais_de_sao_paulo1.txt',mode='r', encoding='utf-8')
    count = 0
    terminais = [];
    for line in f.readlines():
        count = count + 1
        if count == 1:
            myjson = {"nome":"", "endereco":"", "keywords":[], "coords":[]};
            myjson["nome"] = line.replace("\r\n","").strip().split(':')[1]
        elif count == 2:
            myjson["endereco"] = line.replace("\r\n","").strip().split(':')[1]
        elif count ==3:
            myjson["keywords"] = line.replace("\r\n","").strip().split(':')[1].split(',')
        elif count == 4:
            try:
                results = Geocoder.geocode(myjson["endereco"])
                myjson["coords"] = list(results[0].coordinates)
                print myjson["coords"]
            except:
                print "error in " + line
                pass
        else:
            count = 0
            terminais.append(myjson)
    terminais.append(myjson)
    data = {"terminais": terminais}
    with codecs.open('G:\\Poc-Transporte\\Dados SPTrans\\terminais_de_sp.json', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile)
    print "fim"
if __name__ == '__main__':
    main()
