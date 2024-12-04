import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Caminho para a pasta com os arquivos .xls
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
caminho_pasta = os.path.join(parent_dir, 'Ingressantes e Formandos')

# Lista para armazenar os DataFrames
dataframes = []

# Iterar sobre todos os arquivos .xls na pasta
for arquivo in os.listdir(caminho_pasta):
    if arquivo.endswith('.xls') or arquivo.endswith('.xlsx'):  # Verifica o tipo do arquivo
        caminho_arquivo = os.path.join(caminho_pasta, arquivo)
        
        # Ler o arquivo
        df = pd.read_excel(caminho_arquivo)
        
        # Adicionar o DataFrame à lista
        dataframes.append(df)

# Concatenar todos os DataFrames em um só
resultado = pd.concat(dataframes, ignore_index=True)

# Selecionar as colunas relevantes
dados = resultado[['COD_CURSO', 'NOME_UNIDADE', 'ANO', 'SEXO', 'INGRESSANTES', 'FORMADOS']]

# Remover linhas onde 'ANO' é 'TOTAL'
dados = dados[dados['ANO'] != 'TOTAL']

# Converter a coluna 'COD_CURSO' para strings
dados['COD_CURSO'] = dados['COD_CURSO'].astype(str)

# Codificar a coluna 'COD_CURSO' para valores numéricos
label_encoder = LabelEncoder()
dados['COD_CURSO'] = label_encoder.fit_transform(dados['COD_CURSO'])

# Transformar a coluna 'SEXO' em variável dummy
dados = pd.get_dummies(dados, columns=['SEXO'], drop_first=True)

# Separar as features (X) e os targets (y)
X = dados[['COD_CURSO', 'ANO', 'SEXO_M']]
y_ingressantes = dados['INGRESSANTES']
y_formados = dados['FORMADOS']

# Dividir os dados em conjuntos de treino e teste
X_train, X_test, y_train_ingressantes, y_test_ingressantes = train_test_split(X, y_ingressantes, test_size=0.2, random_state=42)
X_train, X_test, y_train_formados, y_test_formados = train_test_split(X, y_formados, test_size=0.2, random_state=42)

# Treinar o modelo de regressão linear para ingressantes
modelo_ingressantes = LinearRegression()
modelo_ingressantes.fit(X_train, y_train_ingressantes)

# Treinar o modelo de regressão linear para formados
modelo_formados = LinearRegression()
modelo_formados.fit(X_train, y_train_formados)

# Fazer previsões para os próximos anos para cada curso e sexo
anos_futuros = np.arange(2024, 2030)
cursos = dados['COD_CURSO'].unique()
sexos = [0, 1]  # 0 para feminino, 1 para masculino

# Lista para armazenar os resultados
resultados = []

for curso in cursos:
    for sexo in sexos:
        previsoes_ingressantes = modelo_ingressantes.predict(np.hstack([np.full((len(anos_futuros), 1), curso), anos_futuros.reshape(-1, 1), np.full((len(anos_futuros), 1), sexo)]))
        previsoes_formados = modelo_formados.predict(np.hstack([np.full((len(anos_futuros), 1), curso), anos_futuros.reshape(-1, 1), np.full((len(anos_futuros), 1), sexo)]))
        
        curso_original = label_encoder.inverse_transform([curso])[0]
        sexo_str = 'M' if sexo == 1 else 'F'
        
        for ano, ingressantes, formados in zip(anos_futuros, previsoes_ingressantes, previsoes_formados):
            resultados.append({
                'COD_CURSO': curso_original,
                'SEXO': sexo_str,
                'ANO': ano,
                'PREV_INGRESSANTES': ingressantes,
                'PREV_FORMADOS': formados
            })

# Criar um DataFrame com os resultados
df_resultados = pd.DataFrame(resultados)

# Salvar o DataFrame em um arquivo CSV
df_resultados.to_csv('previsoes_cursos.csv', index=False)

print("Previsões salvas em 'previsoes_cursos.csv'")