from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import time


def BA():
    # Configurações do arquivo utilizado
    arquivo = pd.read_csv('app/resources/estados_csv/BA.csv', sep=";")
    arquivo_destino = pd.read_csv('app/resources/sitac_csv/BA.csv', sep=";")

    # Configurações da página de pesquisa
    driver = webdriver.Edge()
    driver.get(
        'https://crea-ba.sitac.com.br/app/view/sight/externo?form=PesquisarProfissionalEmpresa')

    while 'continuação' in driver.page_source:
        input(
            "Por favor, resolva o reCAPTCHA manualmente. Pressione Enter quando terminar.\n")

    def pesquisa(i):
        """ Realiza uma busca clicando no botão de pesquisa """
        campo_cnpj.clear()
        campo_cnpj.send_keys(colunaCNPJ[i])
        botao_pesquisa.click()

    def carregando():
        """ continua se está carregando os resultados da busca """
        return driver.execute_script(
            "return document.body.innerText.includes('Carregando')")

    def reCaptcha():
        """ continua se houve erro de reCAPTCHA """
        return driver.execute_script(
            "return document.body.innerText.includes('reCAPTCHA inválido')"
        )

    def resetar_pagina():
        driver.back()
        time.sleep(0.05)
        driver.forward()
        while True:
            try:
                driver.find_element(By.ID, "CNPJ")
                break
            except:
                pass

    def captura_resultado_pesquisa(i):
        """ Captura o resultado da busca e atualiza na planilha """
        while carregando() == True:
            pass
        if not 'Situação do Registro' in driver.page_source:
            print('Nada localizado')
            colunaSITAC[i] = 'Sem registro'
            colunaSituacao[i] = 'Sem registro'
        else:
            time.sleep(0.5)
            situacao = driver.find_element(
                By.XPATH, "/html/body/div[2]/div/div[4]/div/div[2]/form/div[3]/div[2]/div[1]/div[1]/table/tbody/tr/td[4]").text
            print(situacao)
            colunaSituacao[i] = situacao
            colunaSITAC[i] = 'Registrada no SITAC'

    continua = ''
    while continua not in ('S', 'N'):
        continua = input(
            '\n\n\n\nDeseja pular para o ultimo verificado? (S/N)\n')
        continua = continua.upper()

    continua = continua == 'S'

    driver.find_element(By.ID, "PJ").click()
    campo_cnpj = driver.find_element(By.ID, "CNPJ")
    botao_pesquisa = driver.find_element(By.ID, "PESQUISAR")
    colunaCNPJ = list(arquivo['cnpj'])
    if continua:
        colunaSITAC = list(arquivo_destino['sitac_crea'])
        colunaSituacao = list(arquivo_destino['sit_cadastro_crea'])
    else:
        colunaSITAC = list(arquivo['sitac_crea'])
        colunaSituacao = list(arquivo['sit_cadastro_crea'])

    # Executar as buscas percorrendo a planilha
    for i in range(len(arquivo)):

        if colunaSITAC[i] != "Registrada no SITAC":
            if continua:
                if colunaSITAC[i] in ("Registrada no SITAC", 'Sem registro'):
                    continue
            if i > 0 and i % 100 == 0:
                arquivo_destino['cnpj'] = pd.DataFrame(colunaCNPJ)
                arquivo_destino['sit_cadastro_crea'] = pd.DataFrame(
                    colunaSituacao)
                arquivo_destino['sitac_crea'] = pd.DataFrame(colunaSITAC)
                arquivo['sit_cadastro_crea'] = pd.DataFrame(
                    colunaSituacao)
                arquivo['sitac_crea'] = pd.DataFrame(colunaSITAC)

                arquivo.to_csv(
                    'app/resources/estados_csv/BA.csv', sep=";", index=False)
                arquivo_destino.to_csv(
                    'app/resources/sitac_csv/BA.csv', sep=";", index=False)
            resetar_pagina()
            driver.find_element(By.ID, "PJ").click()
            campo_cnpj = driver.find_element(By.ID, "CNPJ")
            botao_pesquisa = driver.find_element(By.ID, "PESQUISAR")
            pesquisa(i)

            while carregando() or reCaptcha():
                driver.execute_script(
                    'document.getElementById("PESQUISAR").removeAttribute("disabled")')
                if reCaptcha():
                    botao_pesquisa.click()
                else:
                    pass

            captura_resultado_pesquisa(i)
            print('*****************************************\n')

    # Gerar novo arquivo com os resultados
    arquivo_destino['cnpj'] = pd.DataFrame(colunaCNPJ)
    arquivo_destino['sit_cadastro_crea'] = pd.DataFrame(colunaSituacao)
    arquivo_destino['sitac_crea'] = pd.DataFrame(colunaSITAC)
    arquivo['sit_cadastro_crea'] = pd.DataFrame(
        colunaSituacao)
    arquivo['sitac_crea'] = pd.DataFrame(colunaSITAC)

    arquivo.to_csv(
        'app/resources/estados_csv/BA.csv', sep=";", index=False)
    arquivo_destino.to_csv(
        'app/resources/sitac_csv/BA.csv', sep=";", index=False)
    driver.quit()
    return 1


BA()
