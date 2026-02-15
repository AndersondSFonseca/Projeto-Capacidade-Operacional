import pandas as pd
import os
class Dados:
    @staticmethod
    def dado_bruto():
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        caminho = os.path.join(
            base_dir,
            "data",
            "bruto",
            "Technical Support Dataset.csv"
        )

        df = pd.read_csv(caminho, sep=",")
        return df