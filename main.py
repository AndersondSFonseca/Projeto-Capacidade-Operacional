from src.data_processing import tratar_dados, salvar_dado_limpo

def main():
    df_tratado = tratar_dados()
    salvar_dado_limpo(df_tratado)
    print(df_tratado.head())

if __name__ == '__main__':
    main()