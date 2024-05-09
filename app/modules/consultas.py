from selenium.webdriver.common.by import By
from selenium import webdriver
from os import system
import pandas as pd
import time


def consulta_cft(arquivo_csv):
    url = 'https://corporativo.sinceti.net.br/app/view/sight/externo.php?form=PesquisarProfissionalEmpresa'
    df = pd.read_csv(arquivo_csv, sep=";", low_memory=True)

    # Configurações da página de pesquisa
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get(url)
    driver.find_element(By.ID, "PJ").click()
    campo_cnpj = driver.find_element(By.ID, "CNPJ")
    botao_pesquisa = driver.find_element(By.ID, "PESQUISAR")

    def pesquisa():
        """ Realiza uma busca clicando no botão de pesquisa """
        botao_pesquisa.click()

    def atualiza_campo_cnpj(row):
        """ Limpa o campo CNPJ e insere o CNPJ da empresa atual """
        campo_cnpj.clear()
        campo_cnpj.send_keys(df['cnpj'][row])

    def carregando():
        """ Verifica se está carregando os resultados da busca """
        return driver.execute_script(
            "return document.body.innerText.includes('Carregando')")

    def reCaptcha():
        """ Verifica se houve erro de reCAPTCHA """
        return  driver.execute_script(
            "return document.body.innerText.includes('reCAPTCHA inválido')"
        )

    def captura_resultado_pesquisa(i):
        """ Captura o resultado da busca e atualiza na planilha """
        if not 'Situação do Registro' in driver.page_source:
            print('Nada localizado')
            df['sitac_cft'][i] = 'Sem registro'
            df['sit_cadastro_cft'][i] = 'Sem registro'
            #df.loc[i, 'sitac_cft'] = 'Sem registro'
            #df.loc[i, 'sit_cadastro_cft'] = 'Sem registro'
        else:
            situacao = driver.find_element(
                By.XPATH, "/html/body/div[2]/div/div[4]/div/div[2]/form/div[3]/div[2]/div[1]/div/table/tbody/tr/td[3]").text
            print(situacao)
            df['sit_cadastro_cft'][i] = situacao
            df['sitac_cft'][i] = 'Registrada no SITAC'

    progresso = 0

    # Executar as buscas percorrendo a planilha
    for row, col in df.iterrows():
        if pd.isna(df['sitac_cft'][row]) and pd.isna(df['sit_cadastro_cft'][row]):
            atualiza_campo_cnpj(row)
            pesquisa()

            while carregando() or reCaptcha():
                if reCaptcha():
                    botao_pesquisa.click()
                    time.sleep(0.025)
                else:
                    time.sleep(0.025)

            captura_resultado_pesquisa(row)
            system('cls')

    return df