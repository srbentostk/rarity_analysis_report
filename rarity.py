import json
import pandas as pd
from collections import Counter

# Lista para armazenar os dados
data = []

# Carregar os arquivos JSON
for i in range(10000):
    with open(f'{i}.json', 'r', encoding='utf-8') as f:
        data.append(json.load(f))

# Converter a lista em um DataFrame
df = pd.json_normalize(data)

# Remover colunas indesejadas
df = df.drop(columns=['id', 'name', 'description', 'image', 'animation_url'])
stats_columns = [col for col in df.columns if 'properties.stats' in col]
df = df.drop(columns=stats_columns)

# Calcular a raridade dos atributos
rarities = {}

for column in df.columns:
    rarities[column] = dict(Counter(df[column]))

# Calcular a quantidade de stickers não vazios
stickers = ['properties.sticker1', 'properties.sticker2', 'properties.sticker3', 'properties.sticker4', 'properties.sticker5']
df['non_empty_stickers'] = df[stickers].apply(lambda row: sum([1 for sticker in row if sticker != 'Empty']), axis=1)
rarities['non_empty_stickers'] = dict(Counter(df['non_empty_stickers']))

# Salvar o relatório de raridade como um arquivo CSV
with open('rarities_report.csv', 'w', encoding='utf-8') as f:
    for attribute, counts in rarities.items():
        f.write(f'{attribute}\n')
        for value, count in counts.items():
            f.write(f'{value},{count}\n')
        f.write('\n')
