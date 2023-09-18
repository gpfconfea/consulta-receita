# TODO: adicionar função para realizar as tarefas corretas necessárias de acordo com os arquivos locais
# TODO: exibir notificações do sistema com as informações de atualizações


from datetime import datetime
from bs4 import BeautifulSoup
import requests
import os


def checkUpdate():
    print("Checking updates...\n")

    url = "http://200.152.38.155/CNPJ/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    last_update = soup.select('td')[7].text
    last_update = datetime.strptime(last_update, "%Y-%m-%d %H:%M ")

    try:
        with open('app/resources/log.txt', 'r') as file:
            local_update = file.read()
        local_update = datetime.strptime(local_update, "%Y-%m-%d %H:%M:%S")

        if last_update > local_update:
            print(
                'Atualização de dados necessária.\n'
                f'Data dos arquivos atualizads: {last_update}\n'
                f'Data do último download: {local_update}'
            )
        else:
            print(
                'Os dados estão atualizados.\n'
                f'Data dos arquivos atualizads: {last_update}\n'
                f'Data do último download: {local_update}'
            )
    except:
        print(
            'Não foi possível verificar atualização.\n'
            'Verifique se o arquivo `app/resources/log.txt` existe e contém a data de atualização.\n'
        )
        pass

    input("\nPressione ENTER para continuar...")
    os.system("cls")
