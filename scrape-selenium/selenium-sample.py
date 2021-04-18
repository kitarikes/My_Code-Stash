# https://qiita.com/DisneyAladdin/items/be771591c0a06b30a369
import pickle
import chromedriver_binary # nopa
from selenium import webdriver

# WebDriver のオプションを設定する
options = webdriver.ChromeOptions()
options.add_argument('--headless')

print('connectiong to remote browser...')
driver = webdriver.Chrome(options=options)

import pandas as pd 

df = pd.read_csv('teihen-list.csv')

#print(df['link'][0])

#link = df['link'][0]

thumb_img_urls = []
thumb_mov_urls = []
cnt = 0

for link in df['link']:
    driver.get(link)
    try:
        imgs = driver.find_elements_by_css_selector("#img")
        urls = driver.find_elements_by_css_selector("#thumbnail")

        thumb_img_url = [img.get_attribute("src") for img in imgs]
        thumb_mov_url = [url.get_attribute("href") for url in urls]

        print(f'[{cnt}] -> {driver.current_url}')
        thumb_img_url = thumb_img_url[1].split('?')[0]
        thumb_mov_url = thumb_mov_url[0]
        #print(thumb_img_url[1].split('?')[0])
        #print(thumb_mov_url[0])
    except:
        print(f'error in {driver.current_url}')
        thumb_img_url = 'error'
        thumb_mov_url = 'error'

    thumb_img_urls.append(thumb_img_url)
    thumb_mov_urls.append(thumb_mov_url)

    cnt += 1

with open('thumb_img_urls.pickle', 'wb') as web:
  pickle.dump(thumb_img_urls, web)

with open('thumb_mov_urls.pickle', 'wb') as web:
  pickle.dump(thumb_mov_urls, web)

print('len of imgs', 'len of movs')
print(len(thumb_img_urls), len(thumb_mov_urls))
# ブラウザを終了する
driver.quit()
