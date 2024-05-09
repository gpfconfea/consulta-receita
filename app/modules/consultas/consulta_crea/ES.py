from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import time


def ES():
    # Configurações do arquivo utilizado
    arquivo = pd.read_csv('app/resources/estados_csv/ES.csv', sep=";")
    arquivo_destino = pd.read_csv('app/resources/sitac_csv/ES.csv', sep=";")

    # Configurações da página de pesquisa
    driver = webdriver.Edge()
    driver.get(
        'https://creaes.org.br/ServicosOnline/pgConsultaSituacaoEmpresa.aspx')

    colunaCNPJ = list(arquivo['cnpj'])
    # colunaSITAC = list(arquivo['sitac_crea'])
    # colunaSituacao = list(arquivo['sit_cadastro_crea'])
    colunaSITAC = list(arquivo_destino['sitac_crea'])
    colunaSituacao = list(arquivo_destino['sit_cadastro_crea'])

    driver.find_element(
        By.ID, "ctl00_cphLateralEsquerda_ucEsquerda_apAreaPublica_content_ucAreaPublica_imgbtnConsultaSituacaoEmpresa").click()

    def pesquisa(i):
        """ Realiza uma busca clicando no botão de pesquisa """
        campo_cnpj = driver.find_element(By.ID, "ctl00_cphPrincipal_txtCNPJ")
        botao_pesquisa = driver.find_element(
            By.ID, "ctl00_cphPrincipal_imgbtnPesquisarSituacao")
        campo_cnpj.clear()
        campo_cnpj.send_keys(colunaCNPJ[i])
        botao_pesquisa.click()

    def empresa_encontrada():
        return driver.execute_script("return document.getElementById('ctl00_cphPrincipal_div_resultado').style.display != 'none'")

    def captura_resultado_pesquisa(i):
        """ Captura o resultado da busca e atualiza na planilha """

        if not empresa_encontrada():
            print('Nada localizado')
            colunaSITAC[i] = 'Sem registro'
            colunaSituacao[i] = 'Sem registro'
        else:
            time.sleep(0.5)
            situacao = driver.find_element(
                By.ID, "ctl00_cphPrincipal_rptSituacaoEmpresas_ctl00_lblSituacao").text

            situacao = situacao.replace('TIVA', 'TIVO')
            print(situacao)
            colunaSituacao[i] = situacao
            colunaSITAC[i] = 'Registrada no SITAC'

    verifica = ''
    while verifica not in ('S', 'N'):
        verifica = input(
            '\n\n\n\nDeseja pular para o ultimo verificado? (S/N)\n')
        verifica = verifica.upper()

    # Executar as buscas percorrendo a planilha
    for i in range(len(arquivo)):

        if colunaSITAC[i] != "Registrada no SITAC":
            if verifica:
                if colunaSITAC[i] in ("Registrada no SITAC", 'Sem registro'):
                    continue
            if i > 0 and i % 100 == 0:
                arquivo_destino['cnpj'] = pd.DataFrame(colunaCNPJ)
                arquivo_destino['sit_cadastro_crea'] = pd.DataFrame(
                    colunaSituacao)
                arquivo_destino['sitac_crea'] = pd.DataFrame(colunaSITAC)
                arquivo_destino.to_csv(
                    'app/resources/sitac_csv/ES.csv', sep=";", index=False)
            pesquisa(i)
            time.sleep(0.5)

            captura_resultado_pesquisa(i)
            print('*****************************************\n')

    # Gerar novo arquivo com os resultados
    arquivo_destino['cnpj'] = pd.DataFrame(colunaCNPJ)
    arquivo_destino['sit_cadastro_crea'] = pd.DataFrame(colunaSituacao)
    arquivo_destino['sitac_crea'] = pd.DataFrame(colunaSITAC)
    arquivo_destino.to_csv(
        'app/resources/sitac_csv/ES.csv', sep=";", index=False)
    driver.quit()


ES()
