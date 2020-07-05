#!/usr/bin/env python
# coding: utf-8

import time
import pandas as pd
import urllib
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

global ua
ua=UserAgent()
user_agent=ua.chrome

def get_html(browser):
    elem = browser.find_element_by_xpath("//*")
    source_code = elem.get_attribute("outerHTML")
    return source_code

def scroll_browser(browser):
    last_height,new_height=0,1
    while last_height!=new_height:
        ## get the position actual of the browser
        last_height = browser.execute_script("return document.body.scrollHeight")   
        ## drag down the wep page
        browser.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        time.sleep(5)
        ## get the new position of the scroll
        new_height = browser.execute_script("return document.body.scrollHeight")
        ## obtener the html of the page
    source_code=get_html(browser)
    return source_code

def get_links_news(url_base,soup):
    list_url_noticia=[]
    for article in soup.find_all("h2",{"class":"story-item__content-title overflow-hidden"}):
        list_url_noticia.append(url_base+article.find("a").get("href"))
    return list_url_noticia



def scraping_news(list_url_noticia):
    texto=[]
    titulo=[]
    fecha=[]
    fuente=[]
    url=[]
    for url_noticia in list_url_noticia:
        try:
            request = urllib.request.Request(url_noticia, headers = {"User-Agent":user_agent})
            page=urllib.request.urlopen(request)
            statusCode=page.status
            if statusCode==200:
                soup = BeautifulSoup(page, "html.parser")                 
                parrafo=[]
                for i in soup.find_all('p',{'class':'story-content__font--secondary mb-25 title-xs line-h-md mt-20 secondary-font pr-20'}):
                    parrafo.append(i.text.strip()) 
                if parrafo==[]:
                    parrafo=[j.text.strip() for j in soup.find_all("p",{"class":"section-video__subtitle"})]   
                fecha.append(soup.find("time").get("datetime") if len(soup.find_all("time"))>0 else "none")
                fuente.append(url_noticia.split("://")[1].split(".")[0])
                texto.append("\n".join(parrafo)) 
                url.append(url_noticia)
                titulo.append(soup.h1.text)
                print("fecha:{} || fuente:{} || titulo:{} || url:{}".format(fecha[-1],fuente[-1],titulo[-1],url[-1]))
        except:
            titulo.append("none")
            continue
    df=pd.DataFrame()
    df["fuente"]=fuente
    df["fecha"]=fecha
    df["url"]=url
    df["titulo"]=titulo
    df["texto"]=texto
    return df

