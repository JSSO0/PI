import pandas as pd
import os
from IPython.display import display
from google.colab import drive
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, precision_score, recall_score, f1_score
from statsmodels.tsa.arima_model import ARIMA


drive.mount('/content/drive/')

files_base_url = '/content/drive/My Drive/pi data science/e-commerce/'

files = {}

for file in os.listdir(files_base_url):
    files.update({file.split('.')[0]: files_base_url+file})

print([file_name for file_name in files])


lista_compras_df = pd.read_csv(files['olist_order_items_dataset'])
compras_usuario_df = pd.read_csv(files['olist_orders_dataset'])
produtos_df = pd.read_csv(files['olist_products_dataset'])

len(lista_compras_df)

produtos_categorias = pd.merge(lista_compras_df, produtos_df, on='product_id')
contagem = produtos_categorias[[
    'product_category_name']].value_counts().reset_index()
contagem.columns = ['product_category_name', 'quantity']

categorias_mais_compradas = pd.DataFrame(contagem)
categorias_mais_compradas


sns.set(style="whitegrid")

plt.figure(figsize=(12, 15))
sns.barplot(x='quantity', y='product_category_name',
            data=categorias_mais_compradas, palette='viridis')

plt.xlabel('Quantidade')
plt.ylabel('Categoria de Produto')
plt.title('Categorias mais Compradas')

# exportar CSV
categorias_mais_compradas.to_csv('categorias_mais_compradas.csv', index=False)


plt.show()

data_produtos_comprados_df = pd.merge(
    lista_compras_df, compras_usuario_df, on='order_id')
data_produtos_comprados_df = data_produtos_comprados_df[[
    'product_id', 'order_approved_at']]
categorias = produtos_df[['product_id', 'product_category_name']]
data_produtos_comprados_categorias_df = pd.merge(
    data_produtos_comprados_df, categorias, on='product_id')

data_produtos_comprados_categorias_df['order_approved_at'] = pd.to_datetime(
    data_produtos_comprados_categorias_df['order_approved_at'])

data_produtos_comprados_categorias_df['year'] = data_produtos_comprados_categorias_df['order_approved_at'].dt.year
data_produtos_comprados_categorias_df['month'] = data_produtos_comprados_categorias_df['order_approved_at'].dt.month

data_produtos_comprados_categorias_df = data_produtos_comprados_categorias_df.groupby(
    ['year', 'month', 'product_category_name']).size().reset_index(name='quantidade')

data_produtos_comprados_categorias_df = data_produtos_comprados_categorias_df.dropna()

display(data_produtos_comprados_categorias_df)


df = pd.DataFrame(data_produtos_comprados_categorias_df)

df['year'] = df['year'].astype(np.float64)
df['month'] = df['month'].astype(np.float64)

model = ARIMA(df['quantidade'], order=(1, 1, 1))
model.fit()

pred = model.predict(start=2018.11, end=2018.12)

saude_novembro = pred.loc[(pred['month'] == 11) & (
    pred['product_category_name'] == 'saude')]['quantidade']

print(saude_novembro)

temporada = data_produtos_comprados_categorias_df[
    (data_produtos_comprados_categorias_df['year'] == 2017) &
    (data_produtos_comprados_categorias_df['month'] == 4)
]

plt.figure(figsize=(20, 10))
sns.barplot(x='product_category_name', y='quantidade', data=temporada)

plt.title('Quantidade de Compras por Categoria em Janeiro de 2017')
plt.xlabel('Categoria de Produto')
plt.ylabel('Quantidade de Compras')

plt.xticks(rotation=45, ha='right')


plt.show()
