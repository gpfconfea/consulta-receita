from modules.consultas import *
from modules.check_update import *
from modules.files_manager import *
from modules.menus import *
from imports import *
from get import *


def runApp():
    option = mainMenu()

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

    elif option == 2:
        lista_url()
        baixa()

    elif option == 3:
        sqlite()
        cnae_sec()

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

    elif option == 5:
        ignore = ["BRASIL.csv"]
        path = os.path.join(os.path.dirname(__file__),
                            'resources', 'estados_csv')
        arquivos = [arquivo for arquivo in os.listdir(
            path) if arquivo.endswith(".csv") and not arquivo in ignore]
        for arquivo in arquivos:
            df = consulta_cft(os.path.join(path, arquivo))
            df.to_csv(os.path.join(path, arquivo), index=False, sep=";")
            del df

    elif option == 6:
        path = os.path.join(os.path.dirname(__file__),
                            'resources', 'estados_csv')
        arquivos = [arquivo for arquivo in os.listdir(
            path) if (arquivo.endswith(".csv") and "BRASIL" not in arquivo)]
        df = pd.DataFrame()
        for arquivo in arquivos:
            print(f"Incluindo dados de {arquivo}...")
            df1 = pd.read_csv(os.path.join(path, arquivo),
                              sep=";", low_memory=False)
            df = pd.concat([df, df1])
            del df1
            os.system("cls")
        print("Salvando arquivo BRASIL.csv...")
        df.to_csv(f"{path}/BRASIL.csv", sep=";", index=False)
        os.system("cls")
        print("Concluído!\n")

    elif option == 7:
        path = os.path.join(os.path.dirname(__file__),
                            'resources', 'estados_csv')
        filtrar_cnae(input("Digte o cnae desejado: "), f"{path}/BRASIL.csv")

    elif option == 8:
        pastas = [
            os.path.join(os.path.dirname(__file__),
                         'cnpj_sqlite', 'dados-publicos'),
            os.path.join(os.path.dirname(__file__),
                         'cnpj_sqlite', 'dados-publicos-zip'),
            os.path.join(os.path.dirname(__file__), 'resources', 'estados_csv')]
        for p in pastas:
            deleteFrom(p, ignore_types=['.txt', '.db', '.db-journal'])

    elif option == 0:
        exit()


if __name__ == "__main__":
    checkUpdate()
    while True:
        runApp()
