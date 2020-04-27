# -*- coding: utf-8 -*- 
import os
import sys
import urllib.request
import requests
import time
from selenium import webdriver
from tqdm import tqdm_notebook
from bs4 import BeautifulSoup
import ast
import pickle
import re

driver = webdriver.Chrome("driver/chromedriver")

index = 1

CLINET_ID = "ZuCdHmuW0kfHPRbtwT0o"
CLIENT_SECRET = "gU40t18rJA"
encText = urllib.parse.quote("주가")
naver_new_link = []


while index < 4:
    news_data= []

    url = "https://openapi.naver.com/v1/search/news?query=" + encText + '&start=' + str(index*10 + 1)
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", CLINET_ID)
    request.add_header("X-Naver-Client-Secret", CLIENT_SECRET)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if rescode == 200:
        result = requests.get(response.geturl(), 
            headers={
                "X-Naver-Client-Id":CLINET_ID,
                "X-Naver-Client-Secret":CLIENT_SECRET
            }
        )
        news_data.append(result.json())
    else:
        print("Error Code:" + rescode)

    for item in news_data[0]['items']:
        link = item['link']
        if "naver" in link:
            naver_new_link.append(link)

    print(index, index*10+1, news_data[0]['total'])
    time.sleep(1)
    if index*10 + 1 < news_data[0]['total']:
        index += 1
    else:
        break

news_page_title = []
news_page_content = []

for n in tqdm_notebook(range(len(naver_new_link))):
    try:
        driver.get(naver_new_link[n])
    except:
        print('timeout')
        continue

    try:
        response = driver.page_source
    except:
        driver.switch_to_alert().accept()
        print('게시글이 삭제된 경우')
        continue

    soup = BeautifulSoup(response, "html.parser")

    title = None

    try:
        item = soup.find('div', class_= 'article_info')
        title = item.find('h3', id= 'articleTitle').get_text()
    except:
        title = "OUTLLINK"
    
    news_page_title.append(title)

    docs = None
    text = ''

    data = soup.find_all('div', {'class': '_article_body_contents'})
    if data:
        for item in data:
            text = text + str(item.find_all(text=True)).strip()
            text = ast.literal_eval(text)
            doc = ' '.join(text)
    else:
        doc = "OUTLINK"
    
    news_page_content.append(doc.replace('\n', ' '))

print(len(news_page_title))
print(len(news_page_content))

with open("naver_news_title.pk", 'wb') as f:
    pickle.dump(news_page_title, f)

with open("naver_news_content.pk", 'wb') as f:
    pickle.dump(news_page_content, f)