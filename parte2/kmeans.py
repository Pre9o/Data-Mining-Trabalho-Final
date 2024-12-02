import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Carregar o arquivo CSV com os dados (após o processamento anterior)
df = pd.read_csv('resultado_unificado.csv')

# Remover linhas com valores NaN
df_clean = df.dropna(subset=['INGRESSANTES_MASC', 'INGRESSANTES_FEM'])

# Selecionar apenas as colunas de ingressantes masculinos e femininos
dados_cluster = df_clean[['INGRESSANTES_MASC', 'INGRESSANTES_FEM']]

# Aplicar o KMeans para separar em 2 grupos
kmeans = KMeans(n_clusters=2, random_state=42)
df_clean['Grupo'] = kmeans.fit_predict(dados_cluster)

# Verificar a distribuição dos cursos nos dois grupos
print(df_clean[['COD_CURSO', 'NOME_UNIDADE', 'Grupo']])

# Visualizar os resultados em um gráfico de dispersão
plt.figure(figsize=(8,6))
plt.scatter(df_clean['INGRESSANTES_MASC'], df_clean['INGRESSANTES_FEM'], c=df_clean['Grupo'], cmap='viridis', s=100)
plt.xlabel('Ingressantes Masculinos')
plt.ylabel('Ingressantes Femininos')
plt.title('K-Means: Separação dos Cursos por Ingressantes Masculinos e Femininos')
plt.colorbar(label='Grupo')
plt.show()

# Salvar o resultado com a coluna 'Grupo' no CSV
df_clean.to_csv('resultado_com_grupos.csv', index=False, encoding='utf-8-sig')

print("K-Means aplicado com sucesso. Resultados salvos em 'resultado_com_grupos.csv'.")
