from modules.check_update import *
from modules.files_manager import *
from modules.menus import *
from imports import *
from get import *


def runApp():
    option = mainMenu()

    if option == 1:
        lista_url()
        baixa()
    
    elif option == 2:
        pastas = [
            os.path.join(os.path.dirname(__file__), 'cnpj_sqlite', 'dados-publicos'),
            os.path.join(os.path.dirname(__file__), 'cnpj_sqlite', 'dados-publicos-zip'),
            os.path.join(os.path.dirname(__file__), 'resources', 'estados_csv')]
        for p in pastas:
            deleteFrom(p, ignore_types=['.txt', '.db'])
    
    elif option == 3:
        sqlite()
        cnae_sec()

    elif option == 4:
        LISTAS = pd.read_json("app/resources/listas.json")
        ESTADOS = LISTAS["listas"]["estados"]
        COLUNAS_CSV = LISTAS["listas"]["colunas_csv"]
        for estado in ESTADOS:
            df = pd.DataFrame(get_estabelecimentos_por_estado(estado), columns=COLUNAS_CSV)
            df.to_csv(f"app/resources/estados_csv/{estado}.csv", index=False, sep=";")

    elif option == 0:
        exit()


if __name__ == "__main__":
    checkUpdate()
    while True:
        runApp()
