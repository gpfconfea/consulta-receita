from modules.menus import confirmMenu
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


def defineColumns(DataFrame):
    DataFrame["sitac_cft"] = ""
    DataFrame["sit_cadastro_cft"] = ""
    DataFrame["sitac_crea"] = ""
    DataFrame["sit_cadastro_crea"] = ""


def cnpjFormat(DataFrame):
    DataFrame.cnpj = DataFrame.cnpj.astype(str).apply(lambda x: x.zfill(14))
    DataFrame.cnpj = DataFrame.cnpj.apply(lambda x: f"{x[:2]}.{x[2:5]}.{x[5:8]}/{x[8:12]}-{x[12:]}")
