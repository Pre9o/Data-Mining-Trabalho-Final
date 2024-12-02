import pandas as pd

df = pd.read_csv('dataset_unified.csv')

# Agrupar pelos 7 primeiros campos e somar os valores das colunas restantes
df_agrupado = df.groupby(["Ano", "Semestre", "Cód. Disciplina", "Cód. Turma", "Professor", "Cód. Curso", "Curso"]).agg({
    "Porcentagem de Aprovado": "sum",
    "Porcentagem de Dispensado": "sum",
    "Porcentagem de Reprovado": "sum",
    "Porcentagem de Tr.Parcial": "sum",
    "Porcentagem de Não Concl.": "sum",
    "Porcentagem de CancMatric": "sum",
    "Porcentagem de Repr.Freq": "sum",
    "Alunos": "sum"
}).reset_index()

# Salvar o resultado em um novo arquivo CSV
df_agrupado.to_csv('processado.csv', index=False)

# Exibir o resultado
print(df_agrupado)