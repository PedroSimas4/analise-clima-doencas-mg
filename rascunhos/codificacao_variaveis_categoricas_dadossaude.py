import pandas as pd
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
import numpy as np

# Carregar os dados (substitua 'dados_cronicas_ses_2015.csv' pelo seu arquivo real)
df = pd.read_csv('dados_cronicas_ses_2015.csv', sep=';')

print("\nColunas disponíveis no DataFrame:")
print(df.columns.tolist())

# Tratar dados ausentes (substituir valores vazios por 'Desconhecido' nas colunas categóricas)
colunas_categoricas = ['sg_sexo', 'tp_raca_cor', 'tp_escolaridade']  # Ajuste conforme suas colunas reais
colunas_existentes = [col for col in colunas_categoricas if col in df.columns]

df[colunas_existentes] = df[colunas_existentes].fillna('Desconhecido')

# Codificação One-Hot para colunas categóricas existentes
if colunas_existentes:  # Verifica se há colunas para codificar
    encoder = OneHotEncoder(sparse_output=False, drop='first')
    encoded_cols = encoder.fit_transform(df[colunas_existentes])
    encoded_df = pd.DataFrame(encoded_cols, columns=encoder.get_feature_names_out(colunas_existentes))
    
    # Adicionar colunas codificadas e remover originais
    df = pd.concat([df.drop(colunas_existentes, axis=1), encoded_df], axis=1)
else:
    print("\nNenhuma coluna categórica encontrada para codificação.")

# Codificação Ordinal para escolaridade (se existir)
if 'tp_escolaridade' in df.columns:
    escolaridade_map = {
        'Desconhecido': 0,
        'de 1 a 3': 1,
        'de 4 a 7': 2,
        'Fundamental': 3,
        'Médio': 4,
        'Superior': 5,
        'Ignora': -1
    }
    df['tp_escolaridade'] = df['tp_escolaridade'].map(escolaridade_map)

print("\nDataFrame após codificação:")
print(df.head())

# Salvar o DataFrame processado
df.to_csv('dados_processados.csv', sep=';', index=False)