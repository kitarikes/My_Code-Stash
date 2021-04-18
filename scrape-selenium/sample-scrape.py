from bs4 import BeautifulSoup
import urllib

import pandas as pd


names = []
counts = []
descriptions = []
links = []
imgurls = []

for n in range(1, 42):

  url = f"https://teihenyoutuber.com/?type=1&page={n}"
  headers = {
         "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
         }
  request = urllib.request.Request(url, headers=headers)
  html = urllib.request.urlopen(request)
  soup = BeautifulSoup(html, 'html.parser')
  userli = soup.select("div[class='user']")

  for i in range(len(userli)):
    name_tmp = userli[i].select("div[class='user_info-name-area']")[0].text
    name = name_tmp.replace('\n', '').replace(' ', '')
    link = userli[i].select("a[class='user_link']")[0].attrs['href']
    imgurl = userli[i].select("a[class='user_link'] img")[0].attrs['src']
    count_tmp = userli[i].select("div[class='user_subscriber-count']")[0].text
    count = count_tmp.split('：')[1].replace('人', '')
    description_tmp = userli[i].select("div[class='user_descriprion-area']")[0].text
    description = description_tmp.replace('\n', '')

    names.append(name)
    links.append(link)
    imgurls.append(imgurl)
    counts.append(count)
    descriptions.append(description)

data = {'name': names, 'count': counts, 'description': descriptions, 'link': links, 'imgurl': imgurls}

df = pd.DataFrame(data)
df.to_csv('teihen-list.csv')
