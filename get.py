import sqlite3
from get_ativos import CNAES_ENG, CNAES_IG


def get_estabelecimentos_por_estado(uf, limit=0):
    uf = uf.upper()
    connection = sqlite3.connect(
        "app\cnpj_sqlite\dados-publicos\cnpj.db")
    cursor = connection.cursor()
    if limit == 0:
        show = cursor.execute(
            f"SELECT * FROM estabelecimento WHERE uf = '{uf}'").fetchall()
    else:
        show = cursor.execute(
            f"SELECT * FROM estabelecimento WHERE uf = '{uf}' LIMIT {limit}").fetchall()
    print(show)


# get_estabelecimentos_por_estado("df")


def deletar_cnaes():
    connection = sqlite3.connect(
        "app\cnpj_sqlite\dados-publicos\cnpj.db")
    cursor = connection.cursor()
    cnaes = cursor.execute(
        f'''
        DELETE FROM cnae WHERE codigo IN {CNAES_IG};
            ''')

# deletar_cnaes()
