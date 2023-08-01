import os
import sys
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'rpa-config')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'rpa-utils')))
import constantes
from log import Log
import arquivo
import pandas as pd
import funcoes

PARAMETROS_VALIDOS = ['ler_pdf','gerar_output']

class Main:
    def __init__(self, acao_desejada):
        self.acao_desejada = acao_desejada
        self.log = Log(constantes.CAMINHO_PASTA_LOGS, logging.INFO, logging.INFO)
    
    def ler_pdf(self):
        nome_arquivo = arquivo.obter_nome_arquivos_pasta(constantes.PASTA_INPUT, filtro_arquivo = '*.pdf')
        resultado =  funcoes.ler_arquivos(nome_arquivo)   
        return resultado
         
    def gerar_output(self, resultado):
        df = pd.DataFrame.from_dict(resultado, orient='columns')
        df.to_excel(f'{constantes.PASTA_OUTPUT}\\output.xlsx', engine='xlsxwriter')
        print("Arquivo de saída gerado com sucesso!")

    def run(self):
        self.resultado = self.ler_pdf()
        if self.acao_desejada == 'ler_pdf':
            self.ler_pdf()  
            print('Oficios lidos com sucesso')    
        if self.acao_desejada == 'gerar_output': 
            self.gerar_output(self.resultado)
            print(self.resultado)    

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in PARAMETROS_VALIDOS:
        main = Main(sys.argv[1])
        main.run()
    else:
        print('====================================================================')
        print('==== Execute qual ação você deseja: [ler_pdf] ou [gerar_output] ====')
        print('====================================================================')
