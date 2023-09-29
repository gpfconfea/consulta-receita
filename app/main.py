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
        pastas = [
            os.path.join(os.path.dirname(__file__),
                         'cnpj_sqlite', 'dados-publicos'),
            os.path.join(os.path.dirname(__file__),
                         'cnpj_sqlite', 'dados-publicos-zip'),
            os.path.join(os.path.dirname(__file__), 'resources', 'estados_csv')]
        for p in pastas:
            deleteFrom(p, ignore_types=['.txt', '.db'])

    elif option == 4:
        sqlite()
        cnae_sec()

    elif option == 5:
        LISTAS = pd.read_json("app/resources/listas.json")
        ESTADOS = LISTAS["listas"]["estados"]
        COLUNAS_CSV = LISTAS["listas"]["colunas_csv"]
        for estado in ESTADOS:
            df = pd.DataFrame(get_estabelecimentos_por_estado(
                estado), columns=COLUNAS_CSV)
            df.to_csv(
                f"app/resources/estados_csv/{estado}.csv", index=False, sep=";")
            del df

    elif option == 0:
        exit()


if __name__ == "__main__":
    checkUpdate()
    while True:
        runApp()
