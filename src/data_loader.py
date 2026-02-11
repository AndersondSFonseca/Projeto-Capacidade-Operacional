import pandas as pd
import os
class Dados:
    def dado_bruto():
        diretorio = os.getcwd()
        dado = os.path.join(diretorio, 'data', 'bruto', 'Technical Support Dataset.csv')
        df = pd.read_csv(dado, sep=',')
        return df