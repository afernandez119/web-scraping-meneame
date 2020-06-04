# -*- coding: utf-8 -*-
"""
Created on Jun 2020

@author: Antonio Fernández Troyano
@website: https://fernandeztroyano.es

Web scraper for the spanish news aggregator Meneame using Selenium and Google Chrome.

It gives you the opportunity to extract the follow data from the frontpage:
    - Title
    - News excerpt
    - Number of clicks
    - Date
    - Number of comments
    - Positive votes
    - Negative votes

If you want to download other information you just need to find the xpath and replicate the structure.

You can configure the following parameters:
    - max_clicks (default 25): number of pages you want to scrape


IMPORTANT: it's necessary to download the drivers for the correct version of your browser. In this case I use Chrome.

Page for downloading your driver version: https://chromedriver.chromium.org/downloads

"""

import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

driver= webdriver.Chrome('./chromedriver.exe')

driver.get('https://www.meneame.net/')

cookie_accept=0 #contador para señalar que se han aceptado las cookies
click_b=0 #clicks que se han realizado a "siguiente página"
max_clicks=25 # máximo número de páginas a visualizar
noticias_df=[] #lista para almacenar las noticias y convertir a dataframe

while True:
    
    if cookie_accept==0:
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="qc-cmp-button"]'))).click()
            cookie_accept=1
        except Exception:
            pass
    
    noticias=driver.find_elements_by_xpath('//div[@class="news-body"]')
    
    for noticia in noticias:
        titulo_noticia=noticia.find_element_by_xpath('.//h2/a').text
        texto_noticia=noticia.find_element_by_xpath('.//div[@class="news-content"]').text
        clicks_not=noticia.find_element_by_xpath('.//span[contains(@id,"clicks-number-")]').text    
        fecha_pub=noticia.find_element_by_xpath('.//span[contains(@title,"enviado: ")]').get_attribute('title').replace('enviado: ','')        
        comentarios=noticia.find_element_by_xpath('.//a[@class="comments"]').text.split()[0]        
        votos_positivos=noticia.find_element_by_xpath('.//span[@class="positive-vote-number"]').text        
        votos_negativos=noticia.find_element_by_xpath('.//span[@class="negative-vote-number"]').text
        #print(titulo_noticia)
        #print(texto_noticia)    
        
        col_keys=["titulo","noticia","clicks","fecha","comentarios","positivos","negativos"]
        values=[titulo_noticia,texto_noticia,clicks_not,fecha_pub,comentarios,votos_positivos,votos_negativos]
        noticia=dict(zip(col_keys,values))
        noticias_df.append(noticia)
        

    if click_b>=max_clicks:
        break
    
    print("\n","Esperando unos segundos......","\n")   
    try:
        bott=driver.find_element_by_xpath('//a[contains(@rel,"next")]')
        bott.click()
        click_b+=1
        sleep(random.uniform(8.0,15.0))

    except:
        break

pd.DataFrame(noticias_df).to_csv('noticias_meneame.csv',encoding='utf-8')    

    



