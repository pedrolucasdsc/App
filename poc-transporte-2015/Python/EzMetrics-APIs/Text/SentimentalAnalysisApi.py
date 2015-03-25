'''
Created on 15/01/2015

@author: pcosta
'''

from bottle import route, run, request
import unirest
from pprint import pprint
@route('/SentimentalAnalysis', method='POST')
def SentimentalAnalysis():
    try:
        text = request.forms.get('text')
        unirest.timeout(60)
        jsonRetorno = {}
    except Exception as e:
        pprint(e)
        jsonRetorno = '{"status":"failed","descricao":""}'
    return jsonRetorno

run(host='10.10.4.27', port=8085)