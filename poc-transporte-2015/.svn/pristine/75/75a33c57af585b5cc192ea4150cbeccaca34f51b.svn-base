'''
Created on 15/01/2015

@author: pcosta
'''

from bottle import route, run, request
import unirest
import json
from pprint import pprint
@route('/FaceRecognition', method='POST')
def FaceRecognition():
    try:
        print "FaceRecognition"
        apikey = request.forms.get('api_key')
        apisecret = request.forms.get('api_secret')

        linkImg = request.forms.get('linkImg')

        unirest.timeout(60)
        response  = unirest.get("https://apius.faceplusplus.com/detection/detect?attribute=glass%2Cpose%2Cgender%2Cage%2Crace%2Csmiling&url=" + linkImg + "&api_key=" + apikey + "&api_secret=" + apisecret,
          headers={
            "Accept": "application/json"
          }
        )
        jsonRetorno = response.body
    except Exception as e:
        pprint(e)
        jsonRetorno = '{"status":"failed","descricao":'+json.dumps(e)+'}'
    return jsonRetorno

run(host='localhost', port=8083)