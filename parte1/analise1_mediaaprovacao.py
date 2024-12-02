import pandas as pd
import matplotlib.pyplot as plt

input_csv = "dataset_final.csv"

df = pd.read_csv(input_csv)

df_cursos = df[["Cód. Curso", "Curso", "Porcentagem de Aprovado"]]  # Correção aqui

df_media_aprovacao = df_cursos.groupby(["Cód. Curso", "Curso"], as_index=False).mean()

output_csv = "analise1_mediaaprovacao.csv"
df_media_aprovacao.to_csv(output_csv, index=False)

df_media_aprovacao = pd.read_csv(output_csv)

df_media_aprovacao = df_media_aprovacao.sort_values(by="Porcentagem de Aprovado", ascending=False)

plt.figure(figsize=(12, 6))
plt.bar(df_media_aprovacao["Curso"], df_media_aprovacao["Porcentagem de Aprovado"], color="lightblue")

plt.title("Porcentagem Média de Aprovação por Curso (em %)", fontsize=16)
plt.xlabel("Cursos", fontsize=12)
plt.ylabel("Porcentagem de Aprovado", fontsize=12)

plt.xticks(rotation=45, ha="right", fontsize=10)

plt.tight_layout()

plt.show()

print(df_media_aprovacao)