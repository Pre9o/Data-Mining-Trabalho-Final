import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn import tree
import matplotlib.pyplot as plt
import os

# Carregar seu dataset (substitua pelo caminho correto do seu arquivo CSV)
current_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(current_dir, 'resultado_unificado.csv')
df = pd.read_csv(file_path)

# Criar novas colunas para as variáveis necessárias
df['TOTAL_INGRESSANTES'] = df['INGRESSANTES_MASC'] + df['INGRESSANTES_FEM']
df['TOTAL_FORMADOS'] = df['FORMADOS_MASC'] + df['FORMADOS_FEM']
df['MULHERES_INGRESSANTES'] = df['INGRESSANTES_FEM']

# Definir a variável 'grupo' com base nas comparações
def definir_grupo(row):
    perc_mulheres_ingressantes = row['MULHERES_INGRESSANTES'] / row['TOTAL_INGRESSANTES'] if row['TOTAL_INGRESSANTES'] > 0 else 0
    perc_formados = row['TOTAL_FORMADOS'] / row['TOTAL_INGRESSANTES'] if row['TOTAL_INGRESSANTES'] > 0 else 0
    
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

df['GRUPO'] = df.apply(definir_grupo, axis=1)

X = df[['TOTAL_INGRESSANTES', 'TOTAL_FORMADOS', 'MULHERES_INGRESSANTES']]
y = df['GRUPO']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f'Acurácia: {accuracy}')
print(classification_report(y_test, y_pred))

plt.figure(figsize=(20,10))
tree.plot_tree(clf, feature_names=X.columns, class_names=['1', '2', '3', '4'], filled=True)
plt.show()