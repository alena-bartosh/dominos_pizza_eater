#!/usr/bin/env python3

import pandas as pd

tsv_path_from = 'dist/dominos_pizza_orders.tsv.gz'
df = pd.read_csv(tsv_path_from, sep='\t', compression='gzip', index_col=0)

df['order_id'] = df['order_id'].str.extract(r'(\d+)')

df['price'] = df['price'].str.extract(r'(\d+\.?\d+)')

size_modification_cols = df['details'].str.split(',', expand=True)
df = df.join(size_modification_cols).rename(columns={0: 'size', 1: 'modification'})

df['datetime'] = pd.to_datetime(df['date'], format='%H:%M %d.%m.%Y')

df = df.loc[df.index.repeat(df['count'])]

df = df.drop(['details', 'date', 'count'], axis=1)

tsv_path_to = 'dist/dominos_pizza_orders_transformed.tsv.gz'
df.to_csv(tsv_path_to, sep='\t', compression='gzip')
