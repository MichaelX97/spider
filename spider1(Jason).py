# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 12:43:04 2018

@author: xhs
"""
import json
import datetime
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

item_value_list = list()
def getHtmlCode(url):  # 该方法传入url，返回url对应的html的源码
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
    }
    url1 = urllib.request.Request(url, headers=headers)  # Request函数将url添加头部，模拟浏览器访问
    page = urllib.request.urlopen(url1).read()  # 将url页面的源代码保存成字符串
    page = page.decode('UTF-8')  # 字符串转码
    return page


if __name__ == '__main__':
    html = getHtmlCode('http://www.100ppi.com/')
    soup = BeautifulSoup(html, "html5lib")  # BeautifulSoup类解析url源码并返回一个对象
    infol_main = soup.find(attrs={"class":"main"})
    infol_left = infol_main.find(attrs={"class":"m-left"})
    infol_big = infol_left.find(attrs={"class": "bigpic"})
    infol_lnews = infol_big.find(attrs={"class": "lnews"})
    news = infol_lnews.select('a[href^="/focus"]')
    n = len(news)
    for i in range(n):
        web = urllib.parse.urljoin("http://www.100ppi.com",news[i]['href'])
        html = getHtmlCode(web)
        soup = BeautifulSoup(html, "html5lib")
        infol_main = soup.find(attrs={"class": "main"})
        #main
        
        title = infol_main.find(attrs={"class": "tit2"})
        s=title.h1.string.replace("生意社：","")
        title =s
        #title
        
        date = infol_main.find(attrs={"class": "pr-news-tit"})
        s=int(date.span.string.replace("-",""))
        date = s
        #date
        
        infol_border = infol_main.find(attrs={"class": "border1 fl mt10"})
        infol_pac = infol_border.find_all(attrs={"class": "padd_t5 w218"})
        producer = {}
        consumer = {}
        pac = infol_pac[0].ul
        pac = pac.find_all('li')
        m = len(pac)
        for i in range(m):
            s = pac[i].string
            a = s.replace(")","").split("(",1)
            producer[a[1]] = a[0]
        pac = infol_pac[1].ul
        pac = pac.find_all('li')
        m = len(pac)
        for i in range(m):
            s = pac[i].string
            a = s.replace(")","").split("(",1)
            consumer[a[1]] = a[0]    
        #producers and consumer
        item_value_list.append(
        {
            "init_date": date,
            "title": title,  # 去掉"生意社："
            "link": web,
            "producer": json.dumps(producer),
            "consumer": json.dumps(consumer),
            "ods_clt_date": datetime.datetime.now()
        }
    )
    print(item_value_list)        
    
        
        
