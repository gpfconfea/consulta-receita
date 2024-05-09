from modules.consultas import *
from modules.check_update import *
from modules.files_manager import *
from modules.menus import *
from imports import *
from get import *


def runApp():
    option = mainMenu()

    #Baixar e montar banco de dados
    if option == 1:
        ans = confirmMenu(
            '''Esta opção irá apagar a base de dados atual e baixar sua atualização, 
este processo pode levar um tempo, Deseja continuar?'''
        )
        if ans == True:
            pastas = [
                os.path.join(os.path.dirname(__file__),
                             'cnpj_sqlite', 'dados-publicos'),
                os.path.join(os.path.dirname(__file__),
                             'cnpj_sqlite', 'dados-publicos-zip'),
                os.path.join(os.path.dirname(__file__), 'resources', 'estados_csv')]
            for p in pastas:
                deleteFrom(p, ignore_types=['.txt'])
            lista_url()
            baixa()
            sqlite()
            cnae_sec()

    #Baixar dados da Receita Federal
    elif option == 2:
        lista_url()
        baixa()

    #Montar banco de dados SQLite
    elif option == 3:
        sqlite()
        cnae_sec()

    #Extrair .CSV de cada estado
    elif option == 4:
        LISTAS = pd.read_json("app/resources/listas.json")
        ESTADOS = LISTAS["listas"]["estados"]
        COLUNAS_CSV = LISTAS["listas"]["colunas_csv"]
        for estado in ESTADOS:
            print(f"Gerando arquivo de {estado}...")
            show = get_estabelecimentos_por_estado(estado)
            df = pd.DataFrame(show, columns=COLUNAS_CSV)
            formatDataFrame(df)
            df.to_csv(
                f"app/resources/estados_csv/{estado}.csv", index=False, sep=";")
            del df
            os.system("cls")
        print("Concluído!\n")

    #Extrair dados do CFT
    elif option == 5:
        #ignore = ["BRASIL.csv", "BRASIL.parquet", "SP.csv", "RJ.csv", "RS.csv", "SC.csv"]
        path = os.path.join(os.path.dirname(__file__),
                            'resources', 'estados_csv')
        '''arquivos = [arquivo for arquivo in os.listdir(
            path) if arquivo.endswith(".csv") and not arquivo in ignore]'''
        arquivos=   ["SC.csv"] #["RJ.csv"]["RS.csv", "SC.csv"] 
        for arquivo in arquivos:
            df = consulta_cft(os.path.join(path, arquivo))
            '''df.to_csv(os.path.join(path, arquivo), index=False, sep=";")
            del df'''


    #Gerar arquivo final .CSV com todos os estados
    elif option == 6:
        ignore= ["AC.csv", "AL.csv", "AM.csv", "AP.csv", "BA.csv", "CE.csv"]
        path = os.path.join(os.path.dirname(__file__),
                            'resources', 'estados_csv')
        arquivos = [arquivo for arquivo in os.listdir(
            path) if (arquivo.endswith(".csv") and not arquivo in ignore)]
        path2 = os.path.join(os.path.dirname(__file__),
                            'resources', 'sitac_csv')
        arquivo = [arquivo for arquivo in os.listdir(
            path2) if (arquivo.endswith(".csv") and "BRASIL" not in arquivo)]
        df = pd.DataFrame()
        #chunksize = 100
        for arquivo in arquivos:
            print(f"Incluindo dados de {arquivo}...")
            df1 = pd.read_csv(os.path.join(path, arquivo),
                                sep=";", low_memory=True)
            df = pd.concat([df, df1])
            del df1
            os.system("cls")
        print("Salvando arquivo BRASIL.parquet...")
        df.to_parquet(f"{path}/BRASIL.parquet", index=False)
        os.system("cls")
        print("Concluído!\n")

    #Filtrar cnae específico
    elif option == 7:
        path = os.path.join(os.path.dirname(__file__),
                            'resources', 'estados_csv')
        filtrar_cnae(input("Digte o cnae desejado: "), f"{path}/BRASIL.parquet")
 
    
    #Excluir dados locais
    elif option == 8:
        pastas = [
            os.path.join(os.path.dirname(__file__),
                         'cnpj_sqlite', 'dados-publicos'),
            os.path.join(os.path.dirname(__file__),
                         'cnpj_sqlite', 'dados-publicos-zip'),
            os.path.join(os.path.dirname(__file__), 'resources', 'estados_csv')]
        for p in pastas:
            deleteFrom(p, ignore_types=['.txt', '.db', '.db-journal'])
            
    #Sair
    elif option == 0:
        exit()


if __name__ == "__main__":
    checkUpdate()
    while True:
        runApp()
