import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar o dataset com a nova coluna 'grupo' (substitua pelo caminho correto do arquivo CSV)
df = pd.read_csv(r"C:\Users\gabri\WorkSpace\GitHub\Data-Mining-Trabalho-Final\parte2\seu_arquivo_com_grupo.csv")

# Configurar o estilo do gráfico
sns.set(style="whitegrid")

# Criar o gráfico de dispersão
plt.figure(figsize=(10, 6))

# Plotar o gráfico, com diferentes cores para cada grupo
sns.scatterplot(x='TOTAL_INGRESSANTES', y='MULHERES_INGRESSANTES', hue='grupo', palette='Set1', data=df, s=100)

# Títulos e rótulos
plt.title('Gráfico de Dispersão: Ingressantes Total vs. Ingressantes Femininos', fontsize=14)
plt.xlabel('Total de Alunos Ingressantes', fontsize=12)
plt.ylabel('Alunos Ingressantes Femininos', fontsize=12)

# Adicionar uma legenda para os grupos
plt.legend(title='Grupo', loc='upper left')

# Exibir o gráfico
plt.show()
