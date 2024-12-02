import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Carregar os dois arquivos CSV
df_aprovacao = pd.read_csv("analise1_mediaaprovacao.csv")  # CSV com o código do curso e a porcentagem de aprovados
df_ingressantes = pd.read_csv("analise2_ingressantesCT.csv")  # CSV com o código do curso e a quantidade de ingressantes femininos e masculinos

# Renomear as colunas de código do curso para o mesmo nome
df_aprovacao.rename(columns={"Cód. Curso": "COD_CURSO"}, inplace=True)

# Juntar os dois DataFrames usando a coluna 'COD_CURSO', mantendo apenas os cursos presentes em ambos os arquivos
df_merged = pd.merge(df_aprovacao, df_ingressantes, on="COD_CURSO", how="inner")

# Calcular a porcentagem de ingressantes femininos em relação ao total de ingressantes
df_merged["Porcentagem Ingressantes Femininos"] = (df_merged["Ingressantes Femininos"] / 
                                         (df_merged["Ingressantes Femininos"] + df_merged["Ingressantes Masculinos"])) * 100

# Selecionar apenas as colunas de interesse
df_resultado = df_merged[["COD_CURSO", "Curso", "Porcentagem de Aprovado", "Porcentagem Ingressantes Femininos"]]

# Exibir o DataFrame final
print(df_resultado)

# Salvar o resultado em um novo CSV
df_resultado.to_csv("analiseFinal_kmeans.csv", index=False)

# Selecionar as colunas de interesse para o KMeans
X = df_resultado[["Porcentagem Ingressantes Femininos", "Porcentagem de Aprovado"]]

# Aplicar o algoritmo KMeans com 4 clusters
kmeans = KMeans(n_clusters=4, random_state=42)
df_resultado["Cluster"] = kmeans.fit_predict(X)

# Plotando o gráfico com KMeans
plt.figure(figsize=(12, 8))

# Plotando os pontos coloridos de acordo com o cluster
scatter = plt.scatter(df_resultado["Porcentagem Ingressantes Femininos"], df_resultado["Porcentagem de Aprovado"], 
                      c=df_resultado["Cluster"], cmap='viridis', marker='o', edgecolors='k')

# Plotando os centros dos clusters
centroids = kmeans.cluster_centers_
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=200, marker='x', label="Centros dos Clusters")

# Adicionando título e rótulos
plt.title("Clusters de Cursos: Ingressantes Femininos vs. Porcentagem de Aprovados", fontsize=16)
plt.xlabel("Porcentagem de Ingressantes Femininos", fontsize=12)
plt.ylabel("Porcentagem de Aprovados", fontsize=12)

# Exibindo os nomes dos cursos no gráfico
for i, row in df_resultado.iterrows():
    plt.text(row["Porcentagem Ingressantes Femininos"], row["Porcentagem de Aprovado"], row["Curso"], 
             fontsize=9, ha='right', color='black')

# Exibir o gráfico
plt.legend()
plt.tight_layout()
plt.show()