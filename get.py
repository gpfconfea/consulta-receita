import sqlite3
from get_ativos import CNAES_ENG, CNAES_IG
import pandas as pd


def get_estabelecimentos_por_estado(uf, limit=0):
    uf = uf.upper()
    connection = sqlite3.connect(
        "app\cnpj_sqlite\dados-publicos\cnpj.db")
    cursor = connection.cursor()
    select = f'''
    SELECT cnpj, nome_fantasia, situacao_cadastral, matriz_filial, data_inicio_atividades, cnae_fiscal, cnae.descricao as cnae_descricao,
    natureza_juridica.codigo as codigo_natjuridica, natureza_juridica.descricao as desc_natjuridica, tipo_logradouro, logradouro, numero,
    complemento, bairro, cep, municipio.descricao as municipio, uf, razao_social,opcao_simples, opcao_mei, porte_empresa, capital_social
    FROM estabelecimento
    JOIN empresas ON estabelecimento.cnpj_basico = empresas.cnpj_basico
    JOIN municipio ON estabelecimento.municipio = municipio.codigo
    JOIN cnae ON estabelecimento.cnae_fiscal = cnae.codigo
    JOIN natureza_juridica ON empresas.natureza_juridica = natureza_juridica.codigo
    JOIN simples ON estabelecimento.cnpj_basico = simples.cnpj_basico
    WHERE situacao_cadastral = '02' AND uf = '{uf}'
    '''

    if limit == 0:
        show = cursor.execute(select).fetchall()
    else:
        show = cursor.execute(
            # f"SELECT * FROM estabelecimento WHERE uf = '{uf}' LIMIT {limit}"
            f"{select} LIMIT {limit}").fetchall()
    # print(show)
    return show


df = pd.DataFrame(get_estabelecimentos_por_estado(uf='ac', limit=150), columns=[
    'cnpj', 'nome_fantasia', 'situacao_cadastral', 'matriz_filial', 'data_inicio_atividades', 'cnae_fiscal', 'cnae_descricao',
    'codigo_natjuridica', 'desc_natjuridica', 'tipo_logradouro', 'logradouro', 'numero', 'complemento', 'bairro', 'cep',
    'municipio', 'uf', 'razao_social', 'opcao_simples', 'opcao_mei', 'porte_empresa', 'capital_social'])


def deletar_cnaes():
    connection = sqlite3.connect(
        "app\cnpj_sqlite\dados-publicos\cnpj.db")
    cursor = connection.cursor()
    cnaes = cursor.execute(
        f'''
        DELETE FROM cnae WHERE codigo IN {CNAES_IG};
            ''')

# deletar_cnaes()
