from modules.check_update import *
from modules.files_manager import *
from modules.menus import *
from get import *
from imports import *


def runApp():
    option = mainMenu()

    if option == 1:
        lista_url()
        baixa()
    
    elif option == 2:
        pastas = [
            os.path.join(os.path.dirname(__file__), 'cnpj_sqlite', 'dados-publicos'),
            os.path.join(os.path.dirname(__file__), 'cnpj_sqlite', 'dados-publicos-zip')]    
        for p in pastas:
            deleteFrom(p, ignore_types=['.txt', '.db', '.zip'])
    
    elif option == 3:
        sqlite()
        cnae_sec()

    elif option == 4:
        exit()


if __name__ == "__main__":
    checkUpdate()
    while True:
        runApp()
