#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      llima
#
# Created:     09/03/2015
# Copyright:   (c) llima 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import codecs, json, unirest
def main():
    dominio = "http://compras.dados.gov.br"
    next_url = "/fornecedores/v1/municipios.json"
    f = codecs.open("G:\\Poc-Transporte\\svn\\Poc-Transporte-2015\\Python\\Outputs\\municipios.txt","w", "utf-8")
    while next_url != "":
        response = unirest.get(dominio + next_url, headers={ "Accept": "application/json"})
        f.write(json.dumps(response.body)+"\n")
        if 'next' in response.body['_links']:
            next_url = response.body['_links']['next']['href']
        else:
            next_url = ""
    f.close()

if __name__ == '__main__':
    main()
