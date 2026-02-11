import pandas as pd
import os
class Dados:
    def carregamento_de_dado():
        diretorio = os.getcwd()
        dado = os.path.join(diretorio,'..', 'data', 'bruto', 'Technical Support Dataset.csv')
        df = pd.read_csv(dado, sep=',')
        return df