"""
O código presente não é a versão final da função.
 utilizaremos a API de extração de dados para gerar
 a data da última extração, que será comparada com
 a data de atualização do site da receita federal.
 """


from datetime import datetime
from bs4 import BeautifulSoup
import requests


def checkUpdate():
    url = "http://200.152.38.155/CNPJ/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    last_update = soup.select('td')[7].text
    last_update = datetime.strptime(last_update, "%Y-%m-%d %H:%M ")
    print(f'Última atualização de dados no site: {last_update}')
