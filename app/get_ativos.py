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


def getAtivos(limit=0):
    connection = sqlite3.connect(
        "app/cnpj_sqlite/dados-publicos/cnpj.db")
    cursor = connection.cursor()
    count = 0
    if limit == 0:
        empresas = cursor.execute(
            f'''
        SELECT * FROM estabelecimento WHERE situacao_cadastral = '02' AND cnae_fiscal IN {CNAES_ENG};
             ''').fetchall()
    else:
        empresas = cursor.execute(
            f'''
            SELECT * FROM estabelecimento WHERE situacao_cadastral = '02' AND cnae_fiscal IN {CNAES_ENG} LIMIT {limit};
                ''').fetchall()

    return empresas


# print(getAtivos())


def clear():

    connection = sqlite3.connect(
        "app/cnpj_sqlite/dados-publicos/cnpj.db")
    cursor = connection.cursor()
    count = 0
    empresas = cursor.execute(
        f'''
            DELETE FROM estabelecimento WHERE situacao_cadastral != '02' OR cnae_fiscal IN {CNAES_IG}''')


# clear()
