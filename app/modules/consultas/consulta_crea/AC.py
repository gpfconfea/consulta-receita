from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import time


def AC():
    # Configurações do arquivo utilizado
    arquivo = pd.read_csv('app/resources/estados_csv/AC.csv', sep=";")
    # Configurações da página de pesquisa
    driver = webdriver.Edge()
    driver.get(
        'https://crea-ac.sitac.com.br/app/view/sight/externo?form=PesquisarProfissionalEmpresa')

    # Aguardand resolver o captcha
    while 'Verificação' in driver.page_source:
        time.sleep(2)
    time.sleep(2)

    driver.find_element(By.ID, "PJ").click()
    campo_cnpj = driver.find_element(By.ID, "CNPJ")
    botao_pesquisa = driver.find_element(By.ID, "PESQUISAR")

    def pesquisa(i):
        """ Realiza uma busca clicando no botão de pesquisa """
        campo_cnpj.clear()
        campo_cnpj.send_keys(arquivo['cnpj'][i])
        botao_pesquisa.click()

    def carregando():
        """ Verifica se está carregando os resultados da busca """
        return driver.execute_script(
            "return document.body.innerText.includes('Carregando')")

    def reCaptcha():
        """ Verifica se houve erro de reCAPTCHA """
        return driver.execute_script(
            "return document.body.innerText.includes('reCAPTCHA inválido')"
        )

    def resetar_pagina():
        driver.back()
        time.sleep(0.05)
        driver.forward()
        time.sleep(0.1)

    def captura_resultado_pesquisa(i):
        """ Captura o resultado da busca e atualiza na planilha """

        if not 'Situação do Registro' in driver.page_source:
            print('Nada localizado')
            arquivo['sitac_crea'][i] = 'Sem registro'
            arquivo['sit_cadastro_crea'][i] = 'Sem registro'
        else:
            time.sleep(0.5)
            situacao = driver.find_element(
                By.XPATH, "/html/body/div[2]/div/div[4]/div/div[2]/form/div[3]/div[2]/div[1]/div/table/tbody/tr/td[3]").text
            print(situacao)
            arquivo['sit_cadastro_crea'][i] = situacao
            arquivo['sitac_crea'][i] = 'Registrada no SITAC'

    # Executar as buscas percorrendo a planilha
    for i in range(len(arquivo)):

        if arquivo['sitac_crea'][i] != "Registrada no SITAC":
            resetar_pagina()
            driver.find_element(By.ID, "PJ").click()
            campo_cnpj = driver.find_element(By.ID, "CNPJ")
            botao_pesquisa = driver.find_element(By.ID, "PESQUISAR")
            pesquisa(i)

            while carregando() or reCaptcha():
                if reCaptcha():
                    print('reCaptcha inválido!')
                    botao_pesquisa.click()
                    time.sleep(0.2)
                else:
                    print('Carregando...')
                    time.sleep(0.2)

            captura_resultado_pesquisa(i)
            print('***************************************** \n')

    # Gerar novo arquivo com os resultados
    arquivo.to_csv('app/resources/estados_csv/AC.csv', sep=";", index=False)
    driver.quit()


AC()
