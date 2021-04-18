import pandas as pd
import pickle

df = pd.read_csv('teihen-list.csv')

print(df['link'][0])

with open('test.pickle', 'wb') as web:
  pickle.dump(df['link'][0], web)
