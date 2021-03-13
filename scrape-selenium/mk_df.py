import pickle
import pandas as pd

df = pd.read_csv('teihen-list.csv')

with open('thumb_mov_urls.pickle', 'rb') as web:
  movs = pickle.load(web)


with open('thumb_img_urls.pickle', 'rb') as web:
  imgs = pickle.load(web)
  #print(techacademy)

df['thumb_mov'] = movs
df['thumb_img'] = imgs

df = df[df['thumb_mov'] != "error"]
df = df[df['thumb_img'] != "https://s2.googleusercontent.com/s2/favicons"]


print(len(df))

df.to_csv("teihen-list-v2.csv", index=False)
