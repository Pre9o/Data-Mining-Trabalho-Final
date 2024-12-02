import pandas as pd
import matplotlib.pyplot as plt

# Carregar o dataset
df = pd.read_csv(r"C:\Users\gabri\OneDrive\Desktop\parte2\resultado_unificado.csv")

# Calcular o total de ingressantes
df['TOTAL_INGRESSANTES'] = df['INGRESSANTES_MASC'] + df['INGRESSANTES_FEM']

# Criar o gráfico de dispersão (scatter plot)
plt.figure(figsize=(10, 6))
plt.scatter(df['TOTAL_INGRESSANTES'], df['INGRESSANTES_FEM'], label='Ingressantes Femininas')

# Adicionar rótulos e título
plt.xlabel('Total de Ingressantes')
plt.ylabel('Ingressantes Femininas')
plt.title('Total de Ingressantes vs Ingressantes Femininas')

# Exibir a legenda
plt.legend()

# Exibir o gráfico
plt.grid(True)
plt.tight_layout()
plt.show()
