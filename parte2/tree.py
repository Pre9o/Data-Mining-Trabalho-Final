import pandas as pd

# Carregar seu dataset (substitua pelo caminho correto do seu arquivo CSV)
df = pd.read_csv(r"C:\Users\gabri\WorkSpace\GitHub\Data-Mining-Trabalho-Final\parte2\resultado_unificado.csv")

# Criar novas colunas para as variáveis necessárias
df['TOTAL_INGRESSANTES'] = df['INGRESSANTES_MASC'] + df['INGRESSANTES_FEM']
df['TOTAL_FORMADOS'] = df['FORMADOS_MASC'] + df['FORMADOS_FEM']
df['MULHERES_INGRESSANTES'] = df['INGRESSANTES_FEM']

# Definir a variável 'grupo' com base nas comparações
# Grupo 1: Mulheres ingressantes > 50% dos ingressantes totais
# Grupo 2: Mulheres ingressantes <= 50% e Formados > 50% dos ingressantes totais
# Grupo 3: Mulheres ingressantes <= 50% e Formados <= 50% dos ingressantes totais
# Grupo 4: Mulheres ingressantes > 50% e Formados <= 50% dos ingressantes totais

def definir_grupo(row):
    # Verificar se temos alunos ingressantes ou formados para evitar divisão por zero
    try:
        perc_mulheres_ingressantes = row['MULHERES_INGRESSANTES'] / row['TOTAL_INGRESSANTES'] if row['TOTAL_INGRESSANTES'] > 0 else 0
        perc_formados = row['TOTAL_FORMADOS'] / row['TOTAL_INGRESSANTES'] if row['TOTAL_INGRESSANTES'] > 0 else 0
    except ZeroDivisionError:
        perc_mulheres_ingressantes = 0
        perc_formados = 0
    
    # Definir os grupos com base nas porcentagens calculadas
    if perc_mulheres_ingressantes > 0.5:
        if perc_formados <= 0.5:
            return '4'
        else:
            return '1'
    else:
        if perc_formados > 0.5:
            return '2'
        else:
            return '3'

# Aplicar a função para criar a nova coluna 'grupo'
df['grupo'] = df.apply(definir_grupo, axis=1)

# Salvar o novo dataset com a coluna 'grupo' em um novo arquivo CSV
df.to_csv('seu_arquivo_com_grupo.csv', index=False)

print("Novo arquivo com a coluna 'grupo' gerado com sucesso!")
