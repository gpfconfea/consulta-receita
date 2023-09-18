from modules.menus import confirmMenu
import os


def deleteFrom(path, ignore_types=[], force=False):
    os.system("cls")
    print(f"Realizando limpeza em: {path}")

    try:
        files_to_remove = [os.path.join(path, file) for file in os.listdir(path) if os.path.splitext(file)[-1] not in ignore_types]
    except:
        print(f'Erro de diretório:\n"{path}" não é um diretório válido. Tente novamente.')
        return False
    if len(files_to_remove) > 0:
        if confirmMenu(f"Deseja visualizar os {len(files_to_remove)} arquivos a serem removidos?"):
            for file in files_to_remove:
                print(file)
        if force == False:
            if confirmMenu(f"Confirma excluir todos os {len(files_to_remove)} arquivos?"):
                for file in files_to_remove:
                    os.remove(file)
            else:
                print(f"Nenhum arquivo deletado de {path}.")
        else:
            for file in files_to_remove:
                os.remove(file)
    else:
        print("Nenhum arquivo para ser deletado.")
