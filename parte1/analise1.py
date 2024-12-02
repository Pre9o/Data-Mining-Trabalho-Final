import pandas as pd
import matplotlib.pyplot as plt

# Nome do arquivo CSV de entrada
input_csv = "dataset_final.csv"

# Carregar o CSV em um DataFrame
df = pd.read_csv(input_csv)

# Selecionar apenas as colunas "Curso" e "Porcentagem de Aprovado"
df_cursos = df[["Curso", "Porcentagem de Aprovado"]]

# Agrupar por curso e calcular a média da porcentagem de aprovação
df_media_aprovacao = df_cursos.groupby("Curso", as_index=False).mean()

# Salvar o resultado em um novo arquivo CSV
output_csv = "analise1_mediaaprovacao.csv"
df_media_aprovacao.to_csv(output_csv, index=False)

# Carregar o DataFrame com as médias de aprovação por curso
df_media_aprovacao = pd.read_csv("analise1_mediaaprovacao.csv")

# Ordenar os cursos pela porcentagem de aprovação para melhor exibição
df_media_aprovacao = df_media_aprovacao.sort_values(by="Porcentagem de Aprovado", ascending=False)

# Configurar o gráfico
plt.figure(figsize=(12, 6))
plt.bar(df_media_aprovacao["Curso"], df_media_aprovacao["Porcentagem de Aprovado"], color="lightblue")

# Adicionar título e rótulos
plt.title("Porcentagem Média de Aprovação por Curso (em %)", fontsize=16)
plt.xlabel("Cursos", fontsize=12)
plt.ylabel("Porcentagem de Aprovado", fontsize=12)

# Rotacionar os rótulos no eixo x para evitar sobreposição
plt.xticks(rotation=45, ha="right", fontsize=10)

# Ajustar layout para melhor apresentação
plt.tight_layout()

# Exibir o gráfico
plt.show()

# Exibir o DataFrame resultante