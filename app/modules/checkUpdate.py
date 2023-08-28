from datetime import datetime
from bs4 import BeautifulSoup
import requests


def checkUpdate():
    url = "http://200.152.38.155/CNPJ/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    last_update = soup.select('td')[7].text
    last_update = datetime.strptime(last_update, "%Y-%m-%d %H:%M ").date()

    if last_update < datetime.now().date():
        print('Os dados estão atualizados!')
        print(f'Última atualização: {last_update}')
    else:
        print('Atualização necessária!')
        print(f'Data de atualização: {last_update}')

checkUpdate()