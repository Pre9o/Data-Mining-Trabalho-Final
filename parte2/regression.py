import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

# Caminho para a pasta com os arquivos .xls
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
caminho_pasta = os.path.join(parent_dir, 'Ingressantes e Formandos')

# Lista para armazenar os DataFrames
dataframes = []

for arquivo in os.listdir(caminho_pasta):
    if arquivo.endswith('.xls') or arquivo.endswith('.xlsx'):  # Verifica o tipo do arquivo
        caminho_arquivo = os.path.join(caminho_pasta, arquivo)
        
        df = pd.read_excel(caminho_arquivo)
        
        dataframes.append(df)

resultado = pd.concat(dataframes, ignore_index=True)

# Selecionar as colunas relevantes
dados = resultado[['COD_CURSO', 'NOME_UNIDADE', 'ANO', 'SEXO', 'INGRESSANTES', 'FORMADOS']]

dados = dados[dados['ANO'] != 'TOTAL']

# Converter a coluna 'ANO' para inteiros
dados['ANO'] = dados['ANO'].astype(int)

curso_nome = "Ciência da Computação - Bacharelado"
dados_curso = dados[dados['NOME_UNIDADE'] == curso_nome]

dados_curso = pd.get_dummies(dados_curso, columns=['SEXO'], drop_first=True)

X = dados_curso[['ANO', 'SEXO_M']]
y_ingressantes = dados_curso['INGRESSANTES']
y_formados = dados_curso['FORMADOS']

X_train, X_test, y_train_ingressantes, y_test_ingressantes = train_test_split(X, y_ingressantes, test_size=0.2, random_state=42)
X_train, X_test, y_train_formados, y_test_formados = train_test_split(X, y_formados, test_size=0.2, random_state=42)

modelo_ingressantes = LinearRegression()
modelo_ingressantes.fit(X_train, y_train_ingressantes)

modelo_formados = LinearRegression()
modelo_formados.fit(X_train, y_train_formados)

anos_futuros = np.arange(2024, 2030)
sexos = [0, 1]  # 0 para feminino, 1 para masculino

resultados = []

for sexo in sexos:
    previsoes_ingressantes = modelo_ingressantes.predict(np.hstack([anos_futuros.reshape(-1, 1), np.full((len(anos_futuros), 1), sexo)]))
    previsoes_formados = modelo_formados.predict(np.hstack([anos_futuros.reshape(-1, 1), np.full((len(anos_futuros), 1), sexo)]))
    
    sexo_str = 'M' if sexo == 1 else 'F'
    
    for ano, ingressantes, formados in zip(anos_futuros, previsoes_ingressantes, previsoes_formados):
        resultados.append({
            'NOME_UNIDADE': curso_nome,
            'SEXO': sexo_str,
            'ANO': ano,
            'PREV_INGRESSANTES': ingressantes,
            'PREV_FORMADOS': formados
        })

df_resultados = pd.DataFrame(resultados)

# Plotar os gráficos
for sexo in ['M', 'F']:
    dados_sexo = dados_curso[dados_curso['SEXO_M'] == (1 if sexo == 'M' else 0)]
    previsoes_sexo = df_resultados[df_resultados['SEXO'] == sexo]
    
    plt.figure(figsize=(10, 5))
    
    plt.plot(dados_sexo['ANO'], dados_sexo['INGRESSANTES'], label='Ingressantes (Dados Originais)', marker='o')
    plt.plot(dados_sexo['ANO'], dados_sexo['FORMADOS'], label='Formados (Dados Originais)', marker='o')
    
    plt.plot(previsoes_sexo['ANO'], previsoes_sexo['PREV_INGRESSANTES'], label='Ingressantes (Previsões)', linestyle='--')
    plt.plot(previsoes_sexo['ANO'], previsoes_sexo['PREV_FORMADOS'], label='Formados (Previsões)', linestyle='--')
    
    plt.title(f'Previsões para {curso_nome} ({sexo})')
    plt.xlabel('Ano')
    plt.ylabel('Número de Estudantes')
    plt.xticks(np.arange(dados_sexo['ANO'].min(), previsoes_sexo['ANO'].max() + 1, 1))
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.savefig(f'previsoes_{curso_nome}_{sexo}.png')
    plt.close()

df_resultados.to_csv('previsoes_cursos.csv', index=False)