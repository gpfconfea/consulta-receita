from modules.menus import confirmMenu
import pandas as pd
import os


def deleteFrom(path, ignore_types=[], force=False):
    os.system("cls")
    print(f"Realizando limpeza em: {path}")

    try:
        files_to_remove = [os.path.join(path, file) for file in os.listdir(path) if os.path.splitext(file)[-1] not in ignore_types]
    except:
        print(f'Erro ao procurar arquivos. Tente novamente.')
        return False
    if len(files_to_remove) > 0:
        if force == False:
            if confirmMenu(f"Deseja visualizar os {len(files_to_remove)} arquivos a serem removidos?"):
                for file in files_to_remove:
                    print(file)
            if confirmMenu(f"Confirma excluir todos os {len(files_to_remove)} arquivos?"):
                for file in files_to_remove:
                    os.remove(file)
            else:
                print(f"Nenhum arquivo deletado de {path}.")
        else:
            for file in files_to_remove:
                os.remove(file)
            print("Arquivos deletados.")
    else:
        print("Nenhum arquivo para ser deletado.")


"""
Funções de padronização para
os arquivos CSV extraídos
"""

def addSitacColumns(df):
    df["sitac_cft"] = ""
    df["sit_cadastro_cft"] = ""
    df["sitac_crea"] = ""
    df["sit_cadastro_crea"] = ""
    df["enquadrado_simei"] = ""


def formatCnpj(df):
    cnpj14 = lambda x: x.zfill(14)
    formated_cnpj = lambda x: f"{x[:2]}.{x[2:5]}.{x[5:8]}/{x[8:12]}-{x[12:]}"
    df.cnpj = df.cnpj.astype(str).apply(cnpj14)
    df.cnpj = df.cnpj.astype(str).apply(formated_cnpj)


def dataInicioAtividades(df):
    date = lambda x: f"{x[:4]}-{x[4:6]}-{x[6:8]}"
    df.data_inicio_atividades = df.data_inicio_atividades.astype(str).apply(date)
    df.data_inicio_atividades = pd.to_datetime(df.data_inicio_atividades)


def formatCnaeFiscal(df):
    cnae = lambda x: f"{x[:5]}/{x[5:]}"
    df.cnae_fiscal = df.cnae_fiscal.astype(str).str.zfill(7)
    df.cnae_fiscal = df.cnae_fiscal.apply(cnae)


def formatCep(df):
    cep = lambda x: f"{x[:5]}-{x[5:]}"
    df.cep = df.cep.astype(str).str.zfill(8)
    df.cep = df.cep.apply(cep)


def formatDataFrame(df):
    formatCep(df)
    formatCnpj(df)
    formatCnaeFiscal(df)
    dataInicioAtividades(df)
    addSitacColumns(df)
