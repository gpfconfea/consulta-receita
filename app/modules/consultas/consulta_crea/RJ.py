from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import time


def RJ():
    # Configurações do arquivo utilizado
    arquivo = pd.read_csv('app/resources/estados_csv/RJ.csv', sep=";")
    arquivo_destino = pd.DataFrame()
    #arquivo_final.to_csv('app/resources/sitac_csv/RN.csv', sep=";")
    # Configurações da página de pesquisa
    driver = webdriver.Edge()
    driver.get(
        'https://portalservicos.crea-rj.org.br/#/app/consultas/empresas')

    # Aguardand resolver o captcha
    if 'Verificação' in driver.page_source:
        input("Por favor, resolva o reCAPTCHA manualmente. Pressione Enter quando terminar.")
        time.sleep(10) 
    
    driver.find_element(By.XPATH, '//*[@id="q-app"]/div/div[2]/main/div/div[2]/div/div[1]/label/div/div').click()
    driver.find_element(By.XPATH, '//*[@id="q-app"]/div/div[2]/main/div/div[2]/div/div[1]/label/div/div/div[1]/div[1]/span').click()
    campo_cnpj = driver.find_element(By.ID, "f_caa49612-a4b1-499d-ac9c-4cd84cce0208" )
    botao_pesquisa = driver.find_element(By.XPATH, '//*[@id="q-app"]/div/div[2]/main/div/div[2]/div/div[3]/div/button/span[2]')
    colunaCNPJ = list(arquivo['cnpj'])
    colunaSITAC = list(arquivo['sitac_crea'])
    colunaSituacao = list(arquivo['sit_cadastro_crea'])
    # colunaSITAC = list(arquivo_destino['sitac_crea'])
    # colunaSituacao = list(arquivo_destino['sit_cadastro_crea'])

    def pesquisa(i):
        """ Realiza uma busca clicando no botão de pesquisa """
        campo_cnpj.clear()
        campo_cnpj.send_keys(arquivo['cnpj'][i])
        botao_pesquisa.click()

    def carregando():
        """ Verifica se está carregando os resultados da busca """
        return driver.execute_script(
            "return document.body.innerText.includes('Carregando')")

    def captura_resultado_pesquisa(i):
        """ Captura o resultado da busca e atualiza na planilha """
        while carregando() == True:
             print('Carregando...')
             time.sleep(0.2)

        if not 'Situação do Registro' in driver.page_source:
            print('Nada localizado')
            colunaSITAC[i] = 'Sem registro'
            colunaSituacao[i] = 'Sem registro'
        else:
            time.sleep(0.5)
            situacao = driver.find_element(
                By.XPATH, "/html/body/div[2]/div/div[4]/div/div[2]/form/div[3]/div[2]/div[1]/div/table/tbody/tr/td[3]").text
            print(situacao)
            colunaSituacao[i] = situacao
            colunaSITAC[i] = 'Registrada no SITAC'

    verifica = ''
    while verifica not in ('S', 'N'):
        verifica = input(
            '\n\n\n\nDeseja pular para o ultimo verificado? (S/N)\n')
        verifica = verifica.upper()

    verifica = verifica == 'S'

    # Executar as buscas percorrendo a planilha
    for i in range(len(arquivo)):

        if arquivo['sitac_crea'][i] != "Registrada no SITAC":
            if verifica:
                if colunaSITAC[i] in ("Registrada no SITAC", 'Sem registro'):
                    continue
            if i > 0 and i % 100 == 0:
                arquivo_destino['cnpj'] = pd.DataFrame(colunaCNPJ)
                arquivo_destino['sit_cadastro_crea'] = pd.DataFrame(
                    colunaSituacao)
                arquivo_destino['sitac_crea'] = pd.DataFrame(colunaSITAC)
                arquivo_destino.to_csv(
                    'app/resources/sitac_csv/RJ.csv', sep=";", index=False)
            #resetar_pagina()
            driver.find_element(By.XPATH, '//*[@id="f_ec0b0b4d-ae41-43f1-80a5-c38ef874540d_1"]').click()
            campo_cnpj = driver.find_element(By.ID, "f_caa49612-a4b1-499d-ac9c-4cd84cce0208" )
            botao_pesquisa = driver.find_element(By.XPATH, '//*[@id="q-app"]/div/div[2]/main/div/div[2]/div/div[3]/div/button/span[2]')
            pesquisa(i)

            captura_resultado_pesquisa(i)
            print('***************************************** \n')

    # Gerar novo arquivo com os resultados
    arquivo_destino = arquivo_destino.drop(columns=['cnpj'])
    arquivo = arquivo.drop(columns=['sitac_crea', 'sit_cadastro_crea'])
    arquivo_final = pd.concat([arquivo, arquivo_destino], axis=1)
    arquivo_final.to_csv(
        'app/resources/sitac_csv/RJ.csv', sep=";", index=False)
    print("\nConsulta Finalizada!")
    driver.quit()


RJ()