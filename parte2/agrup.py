import pandas as pd
import os

# Caminho para a pasta com os arquivos .xls
caminho_pasta = r"C:\Users\gabri\OneDrive\Desktop\teste"

# Lista para armazenar os DataFrames
dataframes = []

# Iterar sobre todos os arquivos .xls na pasta
for arquivo in os.listdir(caminho_pasta):
    if arquivo.endswith('.xls') or arquivo.endswith('.xlsx'):  # Verifica o tipo do arquivo
        caminho_arquivo = os.path.join(caminho_pasta, arquivo)
        
        # Extrair o nome do centro do nome do arquivo (assumindo que está antes do '.xls')
        nome_centro = os.path.splitext(arquivo)[0]
        
        # Ler o arquivo
        df = pd.read_excel(caminho_arquivo)
        
        # Adicionar uma nova coluna com o nome do centro
        df['NOME_CENTRO'] = nome_centro
        
        # Adicionar o DataFrame à lista
        dataframes.append(df)

# Concatenar todos os DataFrames em um só
resultado = pd.concat(dataframes, ignore_index=True)

# Agrupar os dados pelo código do curso e sexo, somando os ingressantes e formados para cada sexo
resultado_agrupado = resultado.groupby(['COD_CURSO', 'NOME_UNIDADE', 'NIVEL_CURSO'], as_index=False).agg({
    'ANO': 'first',  # Vamos manter o primeiro ano (caso seja sempre o mesmo)
    'SEXO': 'first',  # Vamos manter o primeiro sexo (depois vamos pivotar)
    'INGRESSANTES': 'sum',
    'FORMADOS': 'sum'
})

# Pivotar os dados para ter uma linha para cada COD_CURSO com ingressantes e formados por sexo
pivot_resultado = resultado.pivot_table(
    index=['COD_CURSO', 'NOME_UNIDADE', 'NIVEL_CURSO', 'ANO'], 
    columns='SEXO', 
    values=['INGRESSANTES', 'FORMADOS'], 
    aggfunc='sum'
)

# Resetar o índice do DataFrame
pivot_resultado = pivot_resultado.reset_index()

# Ajustar o nome das colunas para algo mais claro
pivot_resultado.columns = [
    'COD_CURSO', 
    'NOME_UNIDADE', 
    'NIVEL_CURSO', 
    'ANO', 
    'INGRESSANTES_MASC', 
    'INGRESSANTES_FEM', 
    'FORMADOS_MASC', 
    'FORMADOS_FEM'
]

# Filtrar apenas as linhas onde o 'ANO' é 'total'
resultado_final = pivot_resultado[pivot_resultado['ANO'] == 'TOTAL']

# Salvar o resultado em um arquivo CSV
resultado_final.to_csv('resultado_unificado.csv', index=False, encoding='utf-8-sig')

print("Todos os arquivos foram combinados, agrupados e filtrados para mostrar apenas os totais. O resultado foi salvo em 'resultado_unificado.csv'")
