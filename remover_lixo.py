import pandas as pd

def process_csv(file_path, output_path):
    # Carregar o arquivo CSV
    df = pd.read_csv(file_path)
    
    # Verificar se há pelo menos 7 colunas
    if df.shape[1] < 7:
        raise ValueError("O arquivo CSV precisa ter pelo menos 7 colunas.")
    
    # Selecionar as últimas 7 colunas
    last_7_cols = df.iloc[:, -8:]
    
    # Selecionar todas as colunas exceto a última dessas 7
    cols_to_sum = last_7_cols.iloc[:, :-1]
    
    # Somar os valores dessas colunas
    row_sums = cols_to_sum.sum(axis=1)
    
    # Filtrar as linhas onde a soma é proxima de 100
    filtered_df = df[row_sums >= 99]
    
    # Salvar o resultado em um novo arquivo CSV
    filtered_df.to_csv(output_path, index=False)
    print(f"Arquivo processado salvo em: {output_path}")

# Exemplo de uso
input_file = "dataset_unified.csv"   # Substitua pelo caminho do seu arquivo
output_file = "sem_lixo.csv"    # Substitua pelo caminho desejado para o arquivo de saída
process_csv(input_file, output_file)