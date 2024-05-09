from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import time




def BA():
    arquivo = pd.read_csv('app/resources/estados_csv/BA.csv', sep=";")
    arquivo_destino = arquivo.copy()
    arquivo_destino['sitac_crea'] = 'Não Verificado'
    arquivo_destino['sit_cadastro_crea'] = 'Não Verificado'

    driver = webdriver.Edge()
    driver.get('https://crea-ba.sitac.com.br/app/view/sight/externo?form=PesquisarProfissionalEmpresa')

    while 'Verificação' in driver.page_source:
        time.sleep(2)
    time.sleep(2)
    
    ini=time.asctime()
    print('Início:', ini)
    WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.ID, "PJ").is_displayed())
    driver.find_element(By.ID, "PJ").click()
    campo_cnpj = driver.find_element(By.ID, "CNPJ")
    botao_pesquisa = driver.find_element(By.ID, "PESQUISAR")

    def pesquisa():
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "PESQUISAR")))
        botao_pesquisa.click()

    def atualiza_campo_cnpj(row):
        time.sleep(0.5)
        campo_cnpj.clear()
        campo_cnpj.send_keys(arquivo_destino.loc[row, 'cnpj'])

    def carregando():
         return driver.execute_script(
            "return document.body.innerText.includes('Carregando')")


    def captura_resultado_pesquisa(row):

        while carregando() == True:
             time.sleep(1)
             print('Carregando...')
             

        if 'Nada localizado' in driver.page_source:
            time.sleep(1)
            print('Nada localizado')
            arquivo_destino.loc[row, 'sitac_crea'] = 'Sem registro'
            arquivo_destino.loc[row, 'sit_cadastro_crea'] = 'Sem registro'
        else:
            time.sleep(2)
            situacao = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[4]/div/div[2]/form/div[3]/div[2]/div[1]/div/table/tbody/tr/td[4]").text
            print(situacao)
            arquivo_destino.loc[row, 'sitac_crea'] = 'Registrada no SITAC'
            arquivo_destino.loc[row, 'sit_cadastro_crea'] = situacao
            

    verifica = ''
    while verifica not in ('S', 'N'):
        verifica = input(
            '\n\n\n\nDeseja pular para o ultimo verificado? (S/N)\n')
        verifica = verifica.upper()

    verifica == 'S'

    for row in arquivo_destino.index:
        if verifica and arquivo_destino.loc[row, 'sitac_crea'] != 'Não Verificado':
            continue
        atualiza_campo_cnpj(row)
        pesquisa()
        time.sleep(2)  
        while carregando():
            print("carregando")
            time.sleep(0.2)
        captura_resultado_pesquisa(row)

        if row > 0 and row % 100 == 0:      
            arquivo_final = pd.concat([arquivo, arquivo_destino[['sitac_crea', 'sit_cadastro_crea']]], axis=1)
            arquivo_final.to_csv('app/resources/sitac_csv/BA2.csv', sep=";", index=False)

    arquivo = arquivo.drop(columns=['sitac_crea', 'sit_cadastro_crea'])
    arquivo_final = pd.concat([arquivo, arquivo_destino[['sitac_crea', 'sit_cadastro_crea']]], axis=1)
    arquivo_final.to_csv('app/resources/sitac_csv/Consulta_BA.csv', sep=";", index=False)
    end=(time.asctime())
    print ("Inicio:", ini,"\nFim:",end)
    print("\nConsulta Finalizada!")
    driver.quit()


BA()