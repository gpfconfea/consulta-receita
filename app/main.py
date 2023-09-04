from cnpj_sqlite.dados_cnpj_baixa import *
from cnpj_sqlite.dados_cnpj_cnae_secundaria import *
from cnpj_sqlite.dados_cnpj_lista_url import *
from cnpj_sqlite.dados_cnpj_para_sqlite import *
from modules.checkUpdate import *


checkUpdate()
lista_url()
baixa()
sqlite()
cnae_sec()
