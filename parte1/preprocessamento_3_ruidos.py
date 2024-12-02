import pandas as pd
import csv

df = pd.read_csv('preprocessado.csv')

# lista das colunas de porcentagens
cols_porcentagem = [
    "Porcentagem de Aprovado", "Porcentagem de Dispensado", "Porcentagem de Reprovado",
    "Porcentagem de Tr.Parcial", "Porcentagem de Não Concl.", "Porcentagem de CancMatric",
    "Porcentagem de Repr.Freq"
]

def ajustar_porcentagens(row):
    total = sum(row[cols_porcentagem])
    if total < 100:
        fator_ajuste = 100 / total
        for col in cols_porcentagem:
            row[col] *= fator_ajuste
    return row

df = df.apply(ajustar_porcentagens, axis=1)

df[cols_porcentagem] = df[cols_porcentagem].round().astype(int)

df.to_csv('dataset_final.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)

print(df)