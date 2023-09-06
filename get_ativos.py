import sqlite3
import json

f = open('app/resources/cnaes_eng.json')
rawJsonEng = json.load(f)
CNAES_ENG = []
for i in rawJsonEng['codes']:
    CNAES_ENG.append(i)
CNAES_ENG = tuple(CNAES_ENG)

g = open('app/resources/cnaes_ig.json')
rawJsonIg = json.load(g)
CNAES_IG = []
for i in rawJsonIg['codes']:
    CNAES_IG.append(i)
CNAES_IG = tuple(CNAES_IG)


def getAtivos():
    connection = sqlite3.connect(
        "app/cnpj_sqlite/dados-publicos/cnpj.db")
    cursor = connection.cursor()
    count = 0
    empresas = cursor.execute(
        f'''
        SELECT * FROM estabelecimento WHERE situacao_cadastral = '02' AND cnae_fiscal IN {CNAES_ENG};
             ''').fetchall()

    print(empresas)


# getAtivos()


def clear():

    connection = sqlite3.connect(
        "app/cnpj_sqlite/dados-publicos/cnpj.db")
    cursor = connection.cursor()
    count = 0
    empresas = cursor.execute(
        "DELETE FROM estabelecimento WHERE situacao_cadastral != '02'")
    empresas = cursor.execute(
        f'''
            DELETE FROM estabelecimento WHERE situacao_cadastral != '02' OR cnae_fiscal IN {CNAES_IG}''')


# clear()
