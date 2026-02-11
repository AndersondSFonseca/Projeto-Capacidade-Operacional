import pandas as pd
import os

diretorio = os.getcwd()
dado = os.path.join(diretorio, 'data', 'bruto', 'Technical Support Dataset.csv')
df = pd.read_csv(dado, sep=',')

print(df)