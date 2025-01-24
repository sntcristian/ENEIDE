import pandas as pd

# Carica i dati
df_train = pd.read_csv('annotations_train.csv')
df_dev = pd.read_csv('annotations_dev.csv')
df_test = pd.read_csv('annotations_test.csv')

# Aggiungi la colonna 'split'
df_train['split'] = 'train'
df_dev['split'] = 'dev'
df_test['split'] = 'test'

df_combined = pd.concat([df_train, df_dev, df_test])

split_size = len(df_combined) // 3
df_part1 = df_combined.iloc[:split_size]
df_part2 = df_combined.iloc[split_size:2*split_size]
df_part3 = df_combined.iloc[2*split_size:]

# Se le dimensioni non sono esattamente divisibili per tre, aggiusta le parti rimanenti
remainder = len(df_combined) % 3
if remainder:
    df_part3 = df_combined.iloc[2*split_size:]

df_part1.to_csv('extra_annotations1_test.csv', index=False)

# Salva la Parte 2
df_part2.to_csv('extra_annotations2_test.csv', index=False)

# Salva la Parte 3
df_part3.to_csv('extra_annotations3_test.csv', index=False)