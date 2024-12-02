import pandas as pd
import csv

# Carregar o arquivo CSV
df = pd.read_csv('preprocessado.csv')

# Lista das colunas de porcentagens
cols_porcentagem = [
    "Porcentagem de Aprovado", "Porcentagem de Dispensado", "Porcentagem de Reprovado",
    "Porcentagem de Tr.Parcial", "Porcentagem de Não Concl.", "Porcentagem de CancMatric",
    "Porcentagem de Repr.Freq"
]

# Função para ajustar as porcentagens
def ajustar_porcentagens(row):
    total = sum(row[cols_porcentagem])
    if total < 100:
        fator_ajuste = 100 / total
        for col in cols_porcentagem:
            row[col] *= fator_ajuste
    return row

# Aplicar a função a cada linha do DataFrame
df = df.apply(ajustar_porcentagens, axis=1)

# Converter para inteiros após o ajuste
df[cols_porcentagem] = df[cols_porcentagem].round().astype(int)
df = df.drop(columns="Cód. Curso")

# Salvar o resultado ajustado
df.to_csv('dataset_final.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)

# Exibir o resultado
print(df)