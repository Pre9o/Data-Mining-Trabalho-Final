import os
import pandas as pd

# Obter o diretório onde o script está sendo executado
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Definir o diretório pai
diretorio_pai = os.path.dirname(diretorio_atual)

# Definir o diretório filho dentro da pasta pai
diretorio_dataset = os.path.join(diretorio_pai, "Ingressantes e Formandos")

# Verificar se a pasta filha existe, se não, criar
if not os.path.exists(diretorio_dataset):
    os.makedirs(diretorio_dataset)

# Caminho do arquivo .xls dentro da pasta pai
arquivo_xls = os.path.join(diretorio_dataset, "CT Ingressantes e formados por sexo.xls")  # Substitua pelo nome do arquivo .xls

# Verificar se o arquivo .xls existe
if os.path.exists(arquivo_xls):
    # Carregar o arquivo .xls usando pandas
    df = pd.read_excel(arquivo_xls)

    # Caminho do novo arquivo .csv na pasta filha
    arquivo_csv = os.path.join(diretorio_atual, "analise2_ingressantesCT.csv")  # Nome do arquivo CSV desejado

    # Salvar o DataFrame como .csv na pasta filha
    df.to_csv(arquivo_csv, index=False)
    print(f"Arquivo convertido com sucesso: {arquivo_csv}")
else:
    print(f"O arquivo {arquivo_xls} não foi encontrado.")

# Nome do arquivo CSV de entrada
input_csv = "analise2_ingressantesCT.csv"

df['ANO'] = pd.to_numeric(df['ANO'], errors='coerce')

# Filtrar as linhas para os anos 2021, 2022 e 2023
df_filtered = df[df['ANO'].isin([2021, 2022, 2023])]

# Remover as colunas "NIVEL_CURSO" e "FORMADOS"
df_filtered = df_filtered.drop(columns=["NIVEL_CURSO", "FORMADOS"])

# Agrupar por "Cód. Curso", "Nome do Curso", e "SEXO", somando os "INGRESSANTES" para os anos 2021, 2022 e 2023
df_grouped = df_filtered.groupby(["COD_CURSO", "NOME_UNIDADE", "SEXO"], as_index=False)["INGRESSANTES"].sum()

# Agora vamos pivotar para separar ingressantes femininos e masculinos em colunas separadas
df_pivot = df_grouped.pivot_table(index=["COD_CURSO", "NOME_UNIDADE"], columns="SEXO", values="INGRESSANTES", aggfunc="sum").reset_index()

# Renomear as colunas para facilitar a leitura
df_pivot.columns.name = None  # Remove o nome da coluna (SEXO)
df_pivot.rename(columns={"F": "Ingressantes Femininos", "M": "Ingressantes Masculinos"}, inplace=True)

# Exibir o DataFrame final
print(df_pivot)

# Salvar o resultado em um novo arquivo CSV
output_csv = "analise2_ingressantesCT.csv"
df_pivot.to_csv(output_csv, index=False)