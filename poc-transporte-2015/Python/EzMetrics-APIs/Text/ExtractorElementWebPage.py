'''
Created on 29/01/2015

@author: pcosta
'''

from bottle import route, run, request
import unirest
from bs4 import BeautifulSoup as Soup
from pprint import pprint
import json
import sys

@route('/ExtractorElementWebPage', method='POST')
def ExtractorElementWebPage():
    try:
        objJsonFind = request.json
        #objJsonFind = json.loads(jsonFind)
        #if "jsonFind" in objJsonFind:
        #    jsonFind = objJsonFind["jsonFind"]
        unirest.timeout(60)
        response  = unirest.get(objJsonFind["urlWebPage"],
          headers={
            'Accept': 'application/json',
            'Content-Type':'application/json'
          }
        )
        soup = Soup(response.body)

        elements = soup.select(objJsonFind['find'])
        results=[]
        for e in elements:
            if objJsonFind['text']:
                results.append(e.text)
            else:
                results.append(str(e))
        jsonRetorno = {'element':results}

    except Exception as e:
        pprint(e)
        jsonRetorno = '{"status":"failed","descricao":""}'
    return jsonRetorno

run(host='10.10.4.23', port=8084)